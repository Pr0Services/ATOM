"""
============================================================================
CHE·NU™ V69 — XR PACK V1.7
============================================================================
Spec: CHE-NU_XR_PACK_V1_7_TRUE_SIGNALS_EXPLAIN_ONDEMAND_WASM_VERIFY.md

Features:
1. Heatmap based on TRUE SIGNALS per sphere (not just rules)
2. Progressive/On-demand EXPLAIN (by step range)
3. Browser signature verification via WASM Ed25519
4. Support "very large simulations" (100k+ steps)

Principle: XR = READ ONLY. All execution = human. OPA governs build/zip/sign/publish
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import json
import logging

from ..models import (
    SignalSeries, SphereSignals, GlobalMetrics, TrueSignals,
    HeatmapTile, TrueHeatmap,
    ExplainRange, ExplainItem, ExplainIndex,
    WASMVerifyConfig,
    generate_id, compute_hash, sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# SIGNAL GENERATOR
# ============================================================================

class SignalGenerator:
    """
    Generate True Signals from timeline + events.
    
    Per spec: signals.v1.json is SOURCE OF TRUTH
    """
    
    SPHERES = [
        "business", "personal", "government", "creative",
        "community", "social", "entertainment", "team", "scholar"
    ]
    
    def __init__(self):
        self._rule_to_sphere = {
            "budget": "business",
            "revenue": "business",
            "cost": "business",
            "hr": "team",
            "legal": "government",
            "creative": "creative",
            "social": "social",
            "learning": "scholar",
        }
        self._incident_rules = {"sla_breach", "error", "critical", "emergency"}
    
    def generate_from_timeline(
        self,
        timeline: List[Dict[str, Any]],
        events: List[Dict[str, Any]],
        tenant_id: str,
        simulation_id: str,
    ) -> TrueSignals:
        """Generate signals from timeline and events"""
        
        # Initialize sphere series
        sphere_data: Dict[str, List[SignalSeries]] = {
            s: [] for s in self.SPHERES
        }
        global_data: List[GlobalMetrics] = []
        
        # Process timeline
        for i, state in enumerate(timeline):
            step = state.get("step", i)
            
            # Extract sphere-specific signals
            for sphere in self.SPHERES:
                series = SignalSeries(
                    step=step,
                    cost=state.get(f"{sphere}_cost", 0),
                    risk=state.get("risk", 0.1),
                    velocity=state.get("velocity", 1.0),
                    activity=0,
                    incidents=0,
                    quality=1.0,
                )
                sphere_data[sphere].append(series)
            
            # Global metrics
            global_data.append(GlobalMetrics(
                step=step,
                tokens=state.get("tokens", 0),
                latency_ms=state.get("latency_ms", 0),
                cache_hit_rate=state.get("cache_hit_rate", 0),
                policy_denies=state.get("policy_denies", 0),
            ))
        
        # Process events - add activity, incidents
        for event in events:
            step = event.get("step", 0)
            rule = event.get("rule", "")
            sphere = self._rule_to_sphere.get(rule.split("_")[0], "business")
            
            # Find corresponding series
            if sphere in sphere_data and step < len(sphere_data[sphere]):
                sphere_data[sphere][step].activity += 1
                
                if rule in self._incident_rules:
                    sphere_data[sphere][step].incidents += 1
        
        # Build TrueSignals
        signals = TrueSignals(
            tenant_id=tenant_id,
            simulation_id=simulation_id,
            trace_id=generate_id(),
            step_count=len(timeline),
            spheres=[
                SphereSignals(sphere_id=s, series=sphere_data[s])
                for s in self.SPHERES
            ],
            global_metrics=global_data,
        )
        
        logger.info(f"Generated signals: {len(timeline)} steps, {len(self.SPHERES)} spheres")
        return signals


# ============================================================================
# HEATMAP CALCULATOR
# ============================================================================

class HeatmapCalculator:
    """
    Calculate True Heatmap from signals.
    
    Per spec: Normalize scores, calculate overall from weights
    """
    
    DEFAULT_WEIGHTS = {
        "risk": 0.3,
        "cost": 0.25,
        "activity": 0.15,
        "quality": 0.2,
        "incidents": 0.1,
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS
    
    def calculate(self, signals: TrueSignals) -> TrueHeatmap:
        """Calculate heatmap from signals"""
        tiles = []
        
        for sphere_signals in signals.spheres:
            series = sphere_signals.series
            if not series:
                continue
            
            # Aggregate totals
            total_cost = sum(s.cost for s in series)
            total_activity = sum(s.activity for s in series)
            total_incidents = sum(s.incidents for s in series)
            
            # Calculate averages
            avg_risk = sum(s.risk for s in series) / len(series) if series else 0
            avg_velocity = sum(s.velocity for s in series) / len(series) if series else 1
            avg_quality = sum(s.quality for s in series) / len(series) if series else 1
            
            # Normalize scores (0-1)
            scores = {
                "risk": min(1.0, avg_risk),
                "cost": min(1.0, total_cost / 100000) if total_cost > 0 else 0,
                "activity": min(1.0, total_activity / 100) if total_activity > 0 else 0,
                "quality": 1.0 - avg_quality,
                "incidents": min(1.0, total_incidents / 10) if total_incidents > 0 else 0,
            }
            
            # Calculate overall score
            overall = sum(scores[k] * self.weights.get(k, 0) for k in scores)
            scores["overall"] = overall
            
            # Generate sparkline (last N values)
            sparkline = {
                "risk": [s.risk for s in series[-60:]],
                "cost": [s.cost for s in series[-60:]],
                "velocity": [s.velocity for s in series[-60:]],
            }
            
            tile = HeatmapTile(
                sphere_id=sphere_signals.sphere_id,
                risk=avg_risk,
                cost=total_cost,
                velocity=avg_velocity,
                activity=total_activity,
                incidents=total_incidents,
                quality=avg_quality,
                scores=scores,
                sparkline=sparkline,
            )
            tiles.append(tile)
        
        heatmap = TrueHeatmap(
            tenant_id=signals.tenant_id,
            simulation_id=signals.simulation_id,
            trace_id=signals.trace_id,
            tiles=tiles,
        )
        
        logger.info(f"Calculated heatmap: {len(tiles)} tiles")
        return heatmap


# ============================================================================
# EXPLAIN RANGE BUILDER
# ============================================================================

class ExplainRangeBuilder:
    """
    Build ranged explain for on-demand loading.
    
    Per spec: Only load visible window, not entire 100k+ steps
    """
    
    def __init__(self, range_size: int = 500):
        self.range_size = range_size
    
    def build_index(
        self,
        events: List[Dict[str, Any]],
        total_steps: int,
    ) -> Tuple[ExplainIndex, Dict[int, List[ExplainItem]]]:
        """Build explain index and range data"""
        
        # Group events by step
        events_by_step: Dict[int, List[Dict]] = {}
        for event in events:
            step = event.get("step", 0)
            if step not in events_by_step:
                events_by_step[step] = []
            events_by_step[step].append(event)
        
        # Create ranges
        ranges = []
        range_data: Dict[int, List[ExplainItem]] = {}
        
        num_ranges = (total_steps + self.range_size - 1) // self.range_size
        
        for i in range(num_ranges):
            from_step = i * self.range_size
            to_step = min((i + 1) * self.range_size - 1, total_steps - 1)
            
            # Build items for this range
            items = []
            for step in range(from_step, to_step + 1):
                if step in events_by_step:
                    step_events = events_by_step[step]
                    why = list(set(e.get("rule", "") for e in step_events))
                    sphere = step_events[0].get("sphere", "business")
                    
                    # Calculate impact
                    impact = {}
                    for e in step_events:
                        for k, v in e.get("delta", {}).items():
                            impact[k] = impact.get(k, 0) + v
                    
                    items.append(ExplainItem(
                        step=step,
                        why=why,
                        sphere=sphere,
                        impact=impact,
                        confidence=0.8,
                    ))
            
            # Generate file name and hash
            file_name = f"range_{i:04d}.v1.json"
            range_hash = compute_hash(json.dumps([i.__dict__ for i in items], default=str))
            
            ranges.append(ExplainRange(
                range_id=i,
                from_step=from_step,
                to_step=to_step,
                file=file_name,
                sha256=range_hash[:16],
            ))
            range_data[i] = items
        
        index = ExplainIndex(
            mode="ranged",
            range_size=self.range_size,
            ranges=ranges,
        )
        
        logger.info(f"Built explain index: {len(ranges)} ranges")
        return index, range_data


# ============================================================================
# WASM VERIFIER (Mock for server-side / Full implementation in browser)
# ============================================================================

class WASMVerifier:
    """
    WASM Ed25519 verification.
    
    Per spec: XR ne rend rien tant que signature/etag non validés
    """
    
    def __init__(self, config: WASMVerifyConfig = None):
        self.config = config or WASMVerifyConfig()
    
    def create_signature(
        self,
        zip_hash: str,
        private_key: str = "mock_private_key",
    ) -> Dict[str, str]:
        """Create signature for ZIP hash"""
        # In production, use real Ed25519
        signature = compute_hash(f"{zip_hash}:{private_key}")
        
        return {
            "signature_b64": signature,
            "zip_sha256": zip_hash,
            "algorithm": "Ed25519",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def create_pubkey(self, public_key: str = "mock_public_key") -> Dict[str, str]:
        """Create public key file"""
        return {
            "public_key_b64": public_key,
            "algorithm": "Ed25519",
            "key_id": generate_id(),
        }
    
    def verify(
        self,
        signature: Dict[str, str],
        pubkey: Dict[str, str],
        zip_hash: str,
    ) -> bool:
        """Verify signature (mock - real implementation in browser WASM)"""
        # In production, use real Ed25519 verification
        expected = compute_hash(f"{signature['zip_sha256']}:mock_private_key")
        return signature["signature_b64"] == expected and signature["zip_sha256"] == zip_hash


# ============================================================================
# XR PACK V1.7 BUILDER
# ============================================================================

class XRPackV17Builder:
    """
    Complete XR Pack V1.7 builder.
    
    Per spec: signals + heatmap + ranged explain + WASM verify
    """
    
    def __init__(self):
        self.signal_generator = SignalGenerator()
        self.heatmap_calculator = HeatmapCalculator()
        self.explain_builder = ExplainRangeBuilder()
        self.verifier = WASMVerifier()
    
    def build(
        self,
        tenant_id: str,
        simulation_id: str,
        timeline: List[Dict[str, Any]],
        events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Build complete XR Pack V1.7"""
        
        # 1. Generate signals
        signals = self.signal_generator.generate_from_timeline(
            timeline, events, tenant_id, simulation_id,
        )
        
        # 2. Calculate heatmap
        heatmap = self.heatmap_calculator.calculate(signals)
        
        # 3. Build explain ranges
        explain_index, explain_ranges = self.explain_builder.build_index(
            events, len(timeline),
        )
        
        # 4. Create manifest
        manifest = {
            "schema_version": "v1.7",
            "tenant_id": tenant_id,
            "simulation_id": simulation_id,
            "trace_id": generate_id(),
            "created_at": datetime.utcnow().isoformat(),
            "replay_mode": "chunked",
            "explain_mode": "ranged",
            "signals": True,
            "wasm_verify": True,
            "security": {
                "signature": "xr_pack.v1.sig.json",
                "public_key": "xr_pack.v1.pubkey.json",
            },
            "read_only": True,  # XR = READ ONLY
        }
        
        # 5. Create checksums
        checksums = {
            "manifest": compute_hash(manifest),
            "signals": compute_hash(signals.__dict__),
            "heatmap": compute_hash(heatmap.__dict__),
            "explain_index": compute_hash(explain_index.__dict__),
        }
        
        # 6. Create signature
        zip_hash = compute_hash(checksums)
        signature = self.verifier.create_signature(zip_hash)
        pubkey = self.verifier.create_pubkey()
        
        pack = {
            "manifest": manifest,
            "signals": signals,
            "heatmap": heatmap,
            "explain_index": explain_index,
            "explain_ranges": explain_ranges,
            "checksums": checksums,
            "signature": signature,
            "pubkey": pubkey,
        }
        
        logger.info(f"Built XR Pack V1.7: {tenant_id}/{simulation_id}")
        return pack
    
    def verify_pack(self, pack: Dict[str, Any]) -> bool:
        """Verify XR Pack integrity"""
        checksums = pack.get("checksums", {})
        zip_hash = compute_hash(checksums)
        
        return self.verifier.verify(
            pack["signature"],
            pack["pubkey"],
            zip_hash,
        )


# ============================================================================
# FACTORY
# ============================================================================

def create_xr_pack_v17_builder() -> XRPackV17Builder:
    """Create XR Pack V1.7 builder"""
    return XRPackV17Builder()
