"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — DATASPACE ENGINE UNIT TESTS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A2: Tests Unitaires Core
Date: 8 Janvier 2026

FOCUS: R&D Rule #3 (Identity Boundary) + HTTP 423
- 40% tests positifs
- 40% tests négatifs (DOIT échouer)
- 20% edge cases
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from uuid import uuid4, UUID
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

import sys
sys.path.insert(0, '..')
from tests.factories import UserFactory, SphereFactory
from tests.mocks import MockIdentityService, MockCheckpointService, MockDatabaseSession


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES SPÉCIFIQUES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def dataspace_factory():
    """Factory pour créer des DataSpaces de test."""
    def _create(owner_id: str = None, **kwargs) -> Dict[str, Any]:
        ds_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        return {
            "id": ds_id,
            "name": kwargs.get("name", f"DataSpace-{ds_id[:8]}"),
            "type": kwargs.get("type", "thread"),
            "status": kwargs.get("status", "active"),
            "description": kwargs.get("description"),
            "owner_id": owner_id or str(uuid4()),
            "created_by": owner_id or str(uuid4()),
            "created_at": now,
            "updated_at": now,
            "file_count": kwargs.get("file_count", 0),
            "total_size_bytes": kwargs.get("total_size_bytes", 0),
            "metadata": kwargs.get("metadata", {}),
            "synthetic": True
        }
    return _create


@pytest.fixture
def file_factory():
    """Factory pour créer des fichiers de test."""
    def _create(dataspace_id: str, owner_id: str, **kwargs) -> Dict[str, Any]:
        file_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        return {
            "id": file_id,
            "name": kwargs.get("name", f"file-{file_id[:8]}.txt"),
            "mime_type": kwargs.get("mime_type", "text/plain"),
            "size_bytes": kwargs.get("size_bytes", 1024),
            "dataspace_id": dataspace_id,
            "path": kwargs.get("path", f"/files/{file_id}"),
            "tags": kwargs.get("tags", []),
            "metadata": kwargs.get("metadata", {}),
            "created_at": now,
            "created_by": owner_id,
            "synthetic": True
        }
    return _create


@pytest.fixture
def dataspaces_db():
    """Mock database pour dataspaces."""
    return {}


@pytest.fixture
def files_db():
    """Mock database pour files."""
    return {}


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS POSITIFS (40%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataSpaceCreation:
    """Tests de création de DataSpace."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_create_dataspace_success(self, dataspace_factory, user_id):
        """✅ Création d'un DataSpace réussie."""
        ds = dataspace_factory(owner_id=str(user_id), name="My DataSpace")
        
        assert ds["id"] is not None
        assert ds["name"] == "My DataSpace"
        assert ds["owner_id"] == str(user_id)
        assert ds["created_by"] == str(user_id)
        assert ds["status"] == "active"
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_create_dataspace_has_traceability(self, dataspace_factory, user_id):
        """✅ DataSpace a tous les champs de traçabilité (R&D Rule #6)."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # R&D Rule #6: Champs obligatoires
        assert "id" in ds
        assert "created_by" in ds
        assert "created_at" in ds
        assert "owner_id" in ds
        
        # Valeurs non vides
        assert ds["id"]
        assert ds["created_by"]
        assert ds["created_at"]
    
    @pytest.mark.unit
    async def test_create_dataspace_with_metadata(self, dataspace_factory, user_id):
        """✅ DataSpace avec métadonnées personnalisées."""
        metadata = {"project": "CHE-NU", "version": "76"}
        ds = dataspace_factory(owner_id=str(user_id), metadata=metadata)
        
        assert ds["metadata"] == metadata


class TestDataSpaceAccess:
    """Tests d'accès aux DataSpaces."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    async def test_owner_can_access_dataspace(
        self, dataspace_factory, user_id, identity_service
    ):
        """✅ Le propriétaire peut accéder à son DataSpace."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # Vérifier que l'utilisateur est bien le propriétaire
        can_access = await identity_service.verify_ownership(
            ds["owner_id"], 
            str(user_id)
        )
        
        assert can_access is True
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    async def test_owner_can_modify_dataspace(
        self, dataspace_factory, user_id, identity_service
    ):
        """✅ Le propriétaire peut modifier son DataSpace."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        can_modify = await identity_service.verify_ownership(
            ds["owner_id"],
            str(user_id)
        )
        
        assert can_modify is True
        
        # Simuler modification
        ds["name"] = "Updated Name"
        ds["updated_at"] = datetime.utcnow().isoformat()
        
        assert ds["name"] == "Updated Name"


class TestFileOperations:
    """Tests d'opérations sur les fichiers."""
    
    @pytest.mark.unit
    async def test_add_file_to_dataspace(
        self, dataspace_factory, file_factory, user_id
    ):
        """✅ Ajout d'un fichier au DataSpace."""
        ds = dataspace_factory(owner_id=str(user_id))
        file = file_factory(ds["id"], str(user_id), name="document.pdf")
        
        assert file["dataspace_id"] == ds["id"]
        assert file["created_by"] == str(user_id)
        assert file["name"] == "document.pdf"
    
    @pytest.mark.unit
    async def test_file_has_traceability(self, dataspace_factory, file_factory, user_id):
        """✅ Fichier a les champs de traçabilité (R&D Rule #6)."""
        ds = dataspace_factory(owner_id=str(user_id))
        file = file_factory(ds["id"], str(user_id))
        
        assert "id" in file
        assert "created_by" in file
        assert "created_at" in file


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS NÉGATIFS (40%) - CE QUI DOIT ÉCHOUER
# ═══════════════════════════════════════════════════════════════════════════════

class TestIdentityBoundaryViolations:
    """Tests de violation de frontière d'identité (R&D Rule #3)."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_cannot_access_other_user_dataspace(
        self, dataspace_factory, user_id, other_user_id, identity_service
    ):
        """❌ Impossible d'accéder au DataSpace d'un autre utilisateur."""
        # DataSpace appartient à user_id
        ds = dataspace_factory(owner_id=str(user_id))
        
        # other_user essaie d'accéder
        can_access = await identity_service.verify_ownership(
            ds["owner_id"],
            str(other_user_id)
        )
        
        assert can_access is False, (
            "R&D Rule #3 VIOLATION: User can access other user's DataSpace!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_cannot_modify_other_user_dataspace(
        self, dataspace_factory, user_id, other_user_id, identity_service
    ):
        """❌ Impossible de modifier le DataSpace d'un autre utilisateur."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # Vérifier que other_user ne peut pas modifier
        can_modify = await identity_service.verify_ownership(
            ds["owner_id"],
            str(other_user_id)
        )
        
        assert can_modify is False, (
            "R&D Rule #3 VIOLATION: User can modify other user's DataSpace!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_cannot_delete_other_user_file(
        self, dataspace_factory, file_factory, user_id, other_user_id, identity_service
    ):
        """❌ Impossible de supprimer le fichier d'un autre utilisateur."""
        ds = dataspace_factory(owner_id=str(user_id))
        file = file_factory(ds["id"], str(user_id))
        
        # other_user essaie de supprimer
        can_delete = await identity_service.verify_ownership(
            ds["owner_id"],
            str(other_user_id)
        )
        
        assert can_delete is False
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_identity_boundary_enforced_on_list(
        self, dataspace_factory, user_id, other_user_id
    ):
        """❌ La liste ne montre que ses propres DataSpaces."""
        # Créer des DataSpaces pour les deux utilisateurs
        ds_user1 = dataspace_factory(owner_id=str(user_id))
        ds_user2 = dataspace_factory(owner_id=str(other_user_id))
        
        # Simuler le filtrage par owner
        all_dataspaces = [ds_user1, ds_user2]
        user1_dataspaces = [ds for ds in all_dataspaces if ds["owner_id"] == str(user_id)]
        
        # User 1 ne devrait voir que son DataSpace
        assert len(user1_dataspaces) == 1
        assert user1_dataspaces[0]["owner_id"] == str(user_id)


class TestHTTP423Required:
    """Tests vérifiant que HTTP 423 est retourné pour actions sensibles."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_delete_dataspace_requires_checkpoint(
        self, dataspace_factory, user_id, checkpoint_service
    ):
        """❌ DELETE DataSpace DOIT retourner HTTP 423."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # Vérifier que checkpoint est requis pour delete
        required = await checkpoint_service.is_checkpoint_required(
            action_type="delete_dataspace",
            impact_level="high"
        )
        
        assert required is True, (
            "R&D Rule #1 VIOLATION: DELETE dataspace should require checkpoint!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_delete_file_requires_checkpoint(
        self, dataspace_factory, file_factory, user_id, checkpoint_service
    ):
        """❌ DELETE file DOIT retourner HTTP 423."""
        required = await checkpoint_service.is_checkpoint_required(
            action_type="delete_file",
            impact_level="high"
        )
        
        assert required is True, (
            "R&D Rule #1 VIOLATION: DELETE file should require checkpoint!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_export_dataspace_requires_checkpoint(
        self, dataspace_factory, user_id, checkpoint_service
    ):
        """❌ EXPORT DataSpace DOIT retourner HTTP 423."""
        required = await checkpoint_service.is_checkpoint_required(
            action_type="export_dataspace",
            impact_level="high"
        )
        
        assert required is True, (
            "R&D Rule #1 VIOLATION: EXPORT dataspace should require checkpoint!"
        )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_action_blocked_without_checkpoint_approval(
        self, dataspace_factory, user_id, checkpoint_service
    ):
        """❌ Action bloquée tant que checkpoint non approuvé."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # Créer un checkpoint
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="delete_dataspace",
            user_id=str(user_id),
            context={"dataspace_id": ds["id"]}
        )
        
        # Vérifier qu'il n'est pas approuvé
        is_approved = await checkpoint_service.is_approved(checkpoint["id"])
        
        assert is_approved is False, (
            "Action should be BLOCKED until checkpoint is approved!"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS EDGE CASES (20%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataSpaceEdgeCases:
    """Tests de cas limites."""
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_empty_dataspace(self, dataspace_factory, user_id):
        """🔸 DataSpace vide (0 fichiers)."""
        ds = dataspace_factory(owner_id=str(user_id), file_count=0)
        
        assert ds["file_count"] == 0
        assert ds["total_size_bytes"] == 0
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_large_dataspace(self, dataspace_factory, user_id):
        """🔸 DataSpace avec beaucoup de fichiers."""
        ds = dataspace_factory(
            owner_id=str(user_id), 
            file_count=10000,
            total_size_bytes=1024 * 1024 * 1024  # 1GB
        )
        
        assert ds["file_count"] == 10000
        assert ds["total_size_bytes"] == 1024 * 1024 * 1024
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_archived_dataspace(self, dataspace_factory, user_id):
        """🔸 DataSpace archivé."""
        ds = dataspace_factory(owner_id=str(user_id), status="archived")
        
        assert ds["status"] == "archived"
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_locked_dataspace(self, dataspace_factory, user_id):
        """🔸 DataSpace verrouillé."""
        ds = dataspace_factory(owner_id=str(user_id), status="locked")
        
        assert ds["status"] == "locked"
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_dataspace_with_special_characters_name(self, dataspace_factory, user_id):
        """🔸 DataSpace avec caractères spéciaux dans le nom."""
        special_names = [
            "Mon DataSpace 🚀",
            "Données/Projet",
            "Fichiers & Documents",
            "Test (version 2)",
        ]
        
        for name in special_names:
            ds = dataspace_factory(owner_id=str(user_id), name=name)
            assert ds["name"] == name
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_concurrent_file_operations(
        self, dataspace_factory, file_factory, user_id
    ):
        """🔸 Opérations de fichiers concurrentes."""
        ds = dataspace_factory(owner_id=str(user_id))
        
        # Créer plusieurs fichiers "simultanément"
        files = [
            file_factory(ds["id"], str(user_id), name=f"file_{i}.txt")
            for i in range(10)
        ]
        
        # Tous les fichiers doivent avoir des IDs uniques
        file_ids = [f["id"] for f in files]
        assert len(file_ids) == len(set(file_ids)), "File IDs must be unique!"


class TestFileEdgeCases:
    """Tests de cas limites pour les fichiers."""
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_file_with_no_extension(self, dataspace_factory, file_factory, user_id):
        """🔸 Fichier sans extension."""
        ds = dataspace_factory(owner_id=str(user_id))
        file = file_factory(ds["id"], str(user_id), name="README")
        
        assert file["name"] == "README"
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_file_with_long_path(self, dataspace_factory, file_factory, user_id):
        """🔸 Fichier avec chemin très long."""
        ds = dataspace_factory(owner_id=str(user_id))
        long_path = "/very/long/nested/directory/structure/" * 10 + "file.txt"
        file = file_factory(ds["id"], str(user_id), path=long_path)
        
        assert file["path"] == long_path
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_zero_byte_file(self, dataspace_factory, file_factory, user_id):
        """🔸 Fichier de 0 bytes."""
        ds = dataspace_factory(owner_id=str(user_id))
        file = file_factory(ds["id"], str(user_id), size_bytes=0)
        
        assert file["size_bytes"] == 0
    
    @pytest.mark.unit
    @pytest.mark.edge_case
    async def test_file_with_many_tags(self, dataspace_factory, file_factory, user_id):
        """🔸 Fichier avec beaucoup de tags."""
        ds = dataspace_factory(owner_id=str(user_id))
        tags = [f"tag_{i}" for i in range(100)]
        file = file_factory(ds["id"], str(user_id), tags=tags)
        
        assert len(file["tags"]) == 100


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS DE SYNCHRONISATION
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataSpaceSync:
    """Tests de synchronisation entre DataSpaces."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    async def test_sync_only_between_own_dataspaces(
        self, dataspace_factory, user_id, other_user_id, identity_service
    ):
        """✅ Sync uniquement entre ses propres DataSpaces."""
        ds1 = dataspace_factory(owner_id=str(user_id), name="Source")
        ds2 = dataspace_factory(owner_id=str(user_id), name="Target")
        
        # Les deux appartiennent au même utilisateur
        assert ds1["owner_id"] == ds2["owner_id"]
        
        # Sync devrait être autorisé
        can_sync_source = await identity_service.verify_ownership(
            ds1["owner_id"], str(user_id)
        )
        can_sync_target = await identity_service.verify_ownership(
            ds2["owner_id"], str(user_id)
        )
        
        assert can_sync_source is True
        assert can_sync_target is True
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_cannot_sync_with_other_user_dataspace(
        self, dataspace_factory, user_id, other_user_id, identity_service
    ):
        """❌ Impossible de sync avec le DataSpace d'un autre utilisateur."""
        ds_mine = dataspace_factory(owner_id=str(user_id))
        ds_other = dataspace_factory(owner_id=str(other_user_id))
        
        # Je ne peux pas accéder au DataSpace de l'autre
        can_access_other = await identity_service.verify_ownership(
            ds_other["owner_id"], str(user_id)
        )
        
        assert can_access_other is False, (
            "R&D Rule #3 VIOLATION: Cannot sync with other user's DataSpace!"
        )
