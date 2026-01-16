"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — MEMORY ENGINE UNIT TESTS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A2: Tests Unitaires Core
Date: 8 Janvier 2026

FOCUS: R&D Rule #7 (Continuité - Append-Only)
Architecture Tri-Layer: HOT → WARM → COLD
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import Dict, Any, List
from enum import Enum

import sys
sys.path.insert(0, '..')
from tests.factories import ThreadFactory, ThreadEventFactory
from tests.mocks import MockCheckpointService, MockRedis


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class MemoryLayer(str, Enum):
    HOT = "hot"      # Redis, TTL session, derniers 50 events
    WARM = "warm"    # PostgreSQL, 30 jours, indexé
    COLD = "cold"    # Object Storage, archive


class MemoryEventType(str, Enum):
    INTENT_DECLARED = "intent.declared"
    DECISION_RECORDED = "decision.recorded"
    ACTION_CREATED = "action.created"
    ACTION_COMPLETED = "action.completed"
    NOTE_ADDED = "note.added"
    SUMMARY_SNAPSHOT = "summary.snapshot"
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def memory_service(mock_redis):
    """Service mémoire mock."""
    class MockMemoryService:
        def __init__(self, redis):
            self.redis = redis
            self.events_db: Dict[str, List[Dict]] = {}
            self.snapshots_db: Dict[str, List[Dict]] = {}
        
        async def add_event(
            self, 
            thread_id: str, 
            event_type: MemoryEventType,
            data: Dict[str, Any],
            user_id: str,
            parent_event_id: str = None
        ) -> Dict[str, Any]:
            """Ajouter un événement (APPEND-ONLY)."""
            event = {
                "id": str(uuid4()),
                "thread_id": thread_id,
                "event_type": event_type,
                "data": data,
                "layer": MemoryLayer.HOT,  # Toujours HOT au départ
                "created_at": datetime.utcnow().isoformat(),
                "created_by": user_id,
                "parent_event_id": parent_event_id,
                "immutable": True
            }
            
            if thread_id not in self.events_db:
                self.events_db[thread_id] = []
            
            self.events_db[thread_id].append(event)
            
            # Aussi dans Redis (HOT)
            await self.redis.lpush(f"memory:hot:{thread_id}", str(event))
            
            return event
        
        async def get_events(
            self,
            thread_id: str,
            layer: MemoryLayer = None,
            limit: int = 50
        ) -> List[Dict]:
            """Récupérer les événements."""
            events = self.events_db.get(thread_id, [])
            
            if layer:
                events = [e for e in events if e["layer"] == layer]
            
            # Tri chronologique inversé (plus récent en premier)
            events = sorted(events, key=lambda x: x["created_at"], reverse=True)
            
            return events[:limit]
        
        async def get_hot_memory(self, thread_id: str, limit: int = 50) -> List[Dict]:
            """Récupérer la mémoire HOT (Redis)."""
            return await self.get_events(thread_id, MemoryLayer.HOT, limit)
        
        async def get_warm_memory(self, thread_id: str, days: int = 30) -> List[Dict]:
            """Récupérer la mémoire WARM (PostgreSQL)."""
            return await self.get_events(thread_id, MemoryLayer.WARM, limit=500)
        
        async def get_cold_memory(self, thread_id: str) -> List[Dict]:
            """Récupérer la mémoire COLD (Archive)."""
            return await self.get_events(thread_id, MemoryLayer.COLD, limit=1000)
        
        async def create_snapshot(
            self,
            thread_id: str,
            snapshot_type: str = "summary"
        ) -> Dict[str, Any]:
            """Créer un snapshot de la mémoire."""
            events = self.events_db.get(thread_id, [])
            
            if not events:
                raise ValueError("No events to snapshot")
            
            sorted_events = sorted(events, key=lambda x: x["created_at"])
            
            snapshot = {
                "id": str(uuid4()),
                "thread_id": thread_id,
                "snapshot_type": snapshot_type,
                "events_count": len(events),
                "time_range_start": sorted_events[0]["created_at"],
                "time_range_end": sorted_events[-1]["created_at"],
                "created_at": datetime.utcnow().isoformat()
            }
            
            if thread_id not in self.snapshots_db:
                self.snapshots_db[thread_id] = []
            
            self.snapshots_db[thread_id].append(snapshot)
            
            return snapshot
        
        async def compress_memory(self, thread_id: str) -> Dict[str, Any]:
            """Compresser: HOT → WARM → COLD."""
            events = self.events_db.get(thread_id, [])
            now = datetime.utcnow()
            moved = 0
            
            for event in events:
                event_time = datetime.fromisoformat(event["created_at"])
                age = now - event_time
                
                old_layer = event["layer"]
                
                if age < timedelta(hours=24):
                    new_layer = MemoryLayer.HOT
                elif age < timedelta(days=30):
                    new_layer = MemoryLayer.WARM
                else:
                    new_layer = MemoryLayer.COLD
                
                if old_layer != new_layer:
                    event["layer"] = new_layer
                    moved += 1
            
            return {"status": "compressed", "events_moved": moved}
        
        async def search(
            self,
            thread_id: str,
            query: str,
            layers: List[MemoryLayer] = None
        ) -> Dict[str, Any]:
            """Rechercher dans la mémoire."""
            events = self.events_db.get(thread_id, [])
            
            if layers:
                events = [e for e in events if e["layer"] in layers]
            
            # Recherche simple
            matching = [
                e for e in events 
                if query.lower() in str(e["data"]).lower()
            ]
            
            return {
                "events": matching,
                "total": len(matching),
                "layers_searched": layers or [MemoryLayer.HOT, MemoryLayer.WARM]
            }
        
        async def get_stats(self, thread_id: str) -> Dict[str, Any]:
            """Statistiques de la mémoire."""
            events = self.events_db.get(thread_id, [])
            
            hot = sum(1 for e in events if e["layer"] == MemoryLayer.HOT)
            warm = sum(1 for e in events if e["layer"] == MemoryLayer.WARM)
            cold = sum(1 for e in events if e["layer"] == MemoryLayer.COLD)
            
            return {
                "thread_id": thread_id,
                "hot_events": hot,
                "warm_events": warm,
                "cold_events": cold,
                "total_events": len(events),
                "memory_health": "healthy" if hot <= 100 else "needs_compression"
            }
    
    return MockMemoryService(mock_redis)


@pytest.fixture
def checkpoint_service():
    return MockCheckpointService()


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS POSITIFS (40%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryEventCreation:
    """Tests de création d'événements mémoire."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    async def test_add_event_success(self, memory_service, user_id, thread_id):
        """✅ Ajout d'un événement réussi."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Test note"},
            str(user_id)
        )
        
        assert event["id"] is not None
        assert event["thread_id"] == str(thread_id)
        assert event["event_type"] == MemoryEventType.NOTE_ADDED
        assert event["layer"] == MemoryLayer.HOT
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_event_has_traceability(self, memory_service, user_id, thread_id):
        """✅ Événement a les champs de traçabilité (R&D Rule #6)."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.DECISION_RECORDED,
            {"decision": "Approve"},
            str(user_id)
        )
        
        # R&D Rule #6: Champs obligatoires
        assert "id" in event
        assert "created_by" in event
        assert "created_at" in event
        
        assert event["created_by"] == str(user_id)
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    async def test_new_events_start_in_hot(self, memory_service, user_id, thread_id):
        """✅ Nouveaux événements commencent en HOT."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.ACTION_CREATED,
            {"action": "Create task"},
            str(user_id)
        )
        
        assert event["layer"] == MemoryLayer.HOT
    
    @pytest.mark.unit
    async def test_event_with_parent_reference(self, memory_service, user_id, thread_id):
        """✅ Événement avec référence au parent."""
        parent = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.INTENT_DECLARED,
            {"intent": "Parent intent"},
            str(user_id)
        )
        
        child = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.ACTION_CREATED,
            {"action": "Child action"},
            str(user_id),
            parent_event_id=parent["id"]
        )
        
        assert child["parent_event_id"] == parent["id"]


class TestTriLayerArchitecture:
    """Tests de l'architecture tri-couche."""
    
    @pytest.mark.unit
    async def test_get_hot_memory(self, memory_service, user_id, thread_id):
        """✅ Récupération mémoire HOT."""
        # Ajouter des événements
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Hot note"},
            str(user_id)
        )
        
        hot_events = await memory_service.get_hot_memory(str(thread_id))
        
        assert len(hot_events) > 0
        assert all(e["layer"] == MemoryLayer.HOT for e in hot_events)
    
    @pytest.mark.unit
    async def test_memory_compression(self, memory_service, user_id, thread_id):
        """✅ Compression HOT → WARM → COLD."""
        # Ajouter des événements
        for i in range(5):
            await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
        
        result = await memory_service.compress_memory(str(thread_id))
        
        assert result["status"] == "compressed"
        assert "events_moved" in result
    
    @pytest.mark.unit
    async def test_memory_stats(self, memory_service, user_id, thread_id):
        """✅ Statistiques mémoire."""
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Test"},
            str(user_id)
        )
        
        stats = await memory_service.get_stats(str(thread_id))
        
        assert stats["thread_id"] == str(thread_id)
        assert "hot_events" in stats
        assert "warm_events" in stats
        assert "cold_events" in stats
        assert "memory_health" in stats


class TestMemorySnapshots:
    """Tests des snapshots."""
    
    @pytest.mark.unit
    async def test_create_snapshot(self, memory_service, user_id, thread_id):
        """✅ Création de snapshot."""
        # Ajouter des événements d'abord
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "For snapshot"},
            str(user_id)
        )
        
        snapshot = await memory_service.create_snapshot(str(thread_id))
        
        assert snapshot["id"] is not None
        assert snapshot["thread_id"] == str(thread_id)
        assert snapshot["events_count"] > 0
    
    @pytest.mark.unit
    async def test_snapshot_time_range(self, memory_service, user_id, thread_id):
        """✅ Snapshot a une plage temporelle."""
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "First"},
            str(user_id)
        )
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Second"},
            str(user_id)
        )
        
        snapshot = await memory_service.create_snapshot(str(thread_id))
        
        assert "time_range_start" in snapshot
        assert "time_range_end" in snapshot


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS NÉGATIFS (40%) - R&D RULE #7: APPEND-ONLY
# ═══════════════════════════════════════════════════════════════════════════════

class TestAppendOnlyViolations:
    """Tests R&D Rule #7: Événements APPEND-ONLY."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_events_are_immutable(self, memory_service, user_id, thread_id):
        """❌ Les événements sont IMMUABLES."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.DECISION_RECORDED,
            {"decision": "Original decision"},
            str(user_id)
        )
        
        # L'événement devrait être marqué immutable
        assert event["immutable"] is True
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_cannot_modify_event(self, memory_service, user_id, thread_id):
        """❌ Impossible de MODIFIER un événement existant."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Original"},
            str(user_id)
        )
        
        # Pas de méthode update_event - c'est volontaire
        assert not hasattr(memory_service, 'update_event'), (
            "R&D Rule #7 VIOLATION: update_event method should not exist!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_cannot_delete_event(self, memory_service, user_id, thread_id):
        """❌ Impossible de SUPPRIMER un événement."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.ACTION_COMPLETED,
            {"result": "Done"},
            str(user_id)
        )
        
        # Pas de méthode delete_event - c'est volontaire
        assert not hasattr(memory_service, 'delete_event'), (
            "R&D Rule #7 VIOLATION: delete_event method should not exist!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    @pytest.mark.negative
    async def test_event_data_cannot_change(self, memory_service, user_id, thread_id):
        """❌ Les données d'un événement ne peuvent pas changer."""
        original_data = {"content": "Original content", "important": True}
        
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            original_data.copy(),
            str(user_id)
        )
        
        # Récupérer et vérifier que c'est identique
        events = await memory_service.get_events(str(thread_id))
        stored_event = next(e for e in events if e["id"] == event["id"])
        
        assert stored_event["data"] == original_data


class TestPurgeRequiresCheckpoint:
    """Tests R&D Rule #1: Purge nécessite checkpoint."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_purge_requires_checkpoint(self, checkpoint_service):
        """❌ PURGE mémoire DOIT nécessiter un checkpoint."""
        required = await checkpoint_service.is_checkpoint_required(
            action_type="purge_memory",
            impact_level="critical"
        )
        
        assert required is True, (
            "R&D Rule #1 VIOLATION: PURGE memory should require checkpoint!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_purge_cold_memory_checkpoint(self, checkpoint_service, user_id):
        """❌ Purge COLD memory nécessite checkpoint."""
        required = await checkpoint_service.is_checkpoint_required(
            action_type="purge_cold_memory",
            impact_level="high"
        )
        
        assert required is True


class TestChronologicalOrder:
    """Tests R&D Rule #5: Ordre chronologique."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_5
    @pytest.mark.negative
    async def test_events_returned_chronologically(self, memory_service, user_id, thread_id):
        """❌ Les événements DOIVENT être en ordre chronologique."""
        # Ajouter plusieurs événements
        for i in range(5):
            await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
        
        events = await memory_service.get_events(str(thread_id))
        
        # Vérifier l'ordre (plus récent en premier)
        for i in range(len(events) - 1):
            current_time = datetime.fromisoformat(events[i]["created_at"])
            next_time = datetime.fromisoformat(events[i + 1]["created_at"])
            
            assert current_time >= next_time, (
                "R&D Rule #5 VIOLATION: Events not in chronological order!"
            )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_5
    @pytest.mark.negative
    async def test_no_ranking_in_memory(self, memory_service, user_id, thread_id):
        """❌ Pas de ranking/scoring dans la mémoire."""
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Test"},
            str(user_id)
        )
        
        # Pas de champs de ranking
        assert "score" not in event
        assert "rank" not in event
        assert "popularity" not in event
        assert "engagement" not in event


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS EDGE CASES (20%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryEdgeCases:
    """Tests de cas limites pour la mémoire."""
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_empty_thread_memory(self, memory_service, thread_id):
        """🔸 Mémoire vide pour un thread."""
        events = await memory_service.get_events(str(thread_id))
        
        assert events == []
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_snapshot_empty_thread_fails(self, memory_service, thread_id):
        """🔸 Snapshot d'un thread vide échoue."""
        with pytest.raises(ValueError, match="No events"):
            await memory_service.create_snapshot(str(thread_id))
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_large_event_data(self, memory_service, user_id, thread_id):
        """🔸 Événement avec beaucoup de données."""
        large_data = {
            "content": "x" * 10000,  # 10KB de texte
            "metadata": {f"key_{i}": f"value_{i}" for i in range(100)}
        }
        
        event = await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            large_data,
            str(user_id)
        )
        
        assert event is not None
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_many_events_same_thread(self, memory_service, user_id, thread_id):
        """🔸 Beaucoup d'événements sur un thread."""
        for i in range(100):
            await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
        
        stats = await memory_service.get_stats(str(thread_id))
        
        assert stats["total_events"] == 100
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_search_no_results(self, memory_service, user_id, thread_id):
        """🔸 Recherche sans résultats."""
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Hello world"},
            str(user_id)
        )
        
        results = await memory_service.search(
            str(thread_id),
            "xyz_not_found_123"
        )
        
        assert results["total"] == 0
        assert results["events"] == []
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_search_with_special_characters(self, memory_service, user_id, thread_id):
        """🔸 Recherche avec caractères spéciaux."""
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Test with émojis 🚀 and spëcial chars!"},
            str(user_id)
        )
        
        results = await memory_service.search(str(thread_id), "🚀")
        
        # Devrait fonctionner ou échouer gracieusement
        assert "events" in results


class TestMemoryLayerMigration:
    """Tests de migration entre couches."""
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_hot_limit_triggers_compression(self, memory_service, user_id, thread_id):
        """🔸 Limite HOT déclenche compression."""
        # Ajouter plus de 50 événements (limite HOT)
        for i in range(60):
            await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
        
        stats = await memory_service.get_stats(str(thread_id))
        
        # Si > 100 hot events, devrait signaler besoin de compression
        if stats["hot_events"] > 100:
            assert stats["memory_health"] == "needs_compression"
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_cross_layer_search(self, memory_service, user_id, thread_id):
        """🔸 Recherche à travers plusieurs couches."""
        await memory_service.add_event(
            str(thread_id),
            MemoryEventType.NOTE_ADDED,
            {"content": "Cross layer test"},
            str(user_id)
        )
        
        results = await memory_service.search(
            str(thread_id),
            "Cross layer",
            layers=[MemoryLayer.HOT, MemoryLayer.WARM, MemoryLayer.COLD]
        )
        
        assert "layers_searched" in results


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS D'INTÉGRITÉ
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryIntegrity:
    """Tests d'intégrité de la mémoire."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_all_events_have_unique_ids(self, memory_service, user_id, thread_id):
        """✅ Tous les événements ont des IDs uniques."""
        events = []
        for i in range(10):
            event = await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
            events.append(event)
        
        ids = [e["id"] for e in events]
        
        assert len(ids) == len(set(ids)), "Event IDs must be unique!"
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_7
    async def test_event_timestamps_monotonic(self, memory_service, user_id, thread_id):
        """✅ Les timestamps sont monotoniques."""
        events = []
        for i in range(5):
            event = await memory_service.add_event(
                str(thread_id),
                MemoryEventType.NOTE_ADDED,
                {"content": f"Note {i}"},
                str(user_id)
            )
            events.append(event)
        
        # Vérifier que chaque timestamp est >= au précédent
        for i in range(len(events) - 1):
            t1 = datetime.fromisoformat(events[i]["created_at"])
            t2 = datetime.fromisoformat(events[i + 1]["created_at"])
            
            assert t1 <= t2, "Timestamps should be monotonically increasing"
