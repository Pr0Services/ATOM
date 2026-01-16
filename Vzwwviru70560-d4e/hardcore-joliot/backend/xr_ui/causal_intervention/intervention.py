"""
============================================================================
CHE·NU™ V69 — XR CAUSAL INTERVENTION UX (V1.7)
============================================================================
Spec: GPT1/CHE-NU_XR_CAUSAL_INTERVENTION_UX.md

Philosophie: Intervention Sans Risque
L'utilisateur n'agit jamais sur le réel.
En XR, il manipule des Causal Proxies.

Chaque interaction:
- est simulée
- est réversible
- génère un draft artifact
- passe par validation OPA

Mécaniques:
- Grab & Slide
- Ripple Effect
- Causal Magnifier

Modes: Ghost Reality, Risk Heatmap, Causal Threads
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import copy

from ..models import (
    CausalProxy,
    RippleWave,
    InterventionDraft,
    ImpactColor,
    RenderMode,
    InteractionType,
    XRPack,
    generate_id,
    compute_hash,
    sign_xr_pack,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CAUSAL PROXY MANAGER
# ============================================================================

class CausalProxyManager:
    """
    Manage causal proxies.
    
    Per spec: Causal Proxies - représentations physiques de variables causales
    """
    
    def __init__(self):
        self._proxies: Dict[str, CausalProxy] = {}
    
    def create_proxy(
        self,
        slot_id: str,
        name: str,
        value: float,
        shape: str = "sphere",
        position: Tuple[float, float, float] = None,
    ) -> CausalProxy:
        """Create a causal proxy"""
        proxy = CausalProxy(
            proxy_id=generate_id(),
            slot_id=slot_id,
            name=name,
            value=value,
            original_value=value,
            shape=shape,
            position=position or (0.0, 0.0, 0.0),
        )
        
        self._proxies[proxy.proxy_id] = proxy
        return proxy
    
    def grab(self, proxy_id: str) -> Optional[CausalProxy]:
        """Grab a proxy"""
        proxy = self._proxies.get(proxy_id)
        if proxy:
            proxy.is_grabbed = True
            logger.info(f"Grabbed proxy {proxy.name}")
        return proxy
    
    def release(self, proxy_id: str) -> Optional[CausalProxy]:
        """Release a proxy"""
        proxy = self._proxies.get(proxy_id)
        if proxy:
            proxy.is_grabbed = False
            logger.info(f"Released proxy {proxy.name}")
        return proxy
    
    def slide(
        self,
        proxy_id: str,
        new_value: float,
    ) -> Optional[CausalProxy]:
        """
        Slide proxy to new value.
        
        Per spec: Grab & Slide - Déplacement = modification causale
        """
        proxy = self._proxies.get(proxy_id)
        if proxy and proxy.is_grabbed:
            proxy.value = new_value
            proxy.is_modified = proxy.value != proxy.original_value
            logger.info(f"Slid {proxy.name}: {proxy.original_value} → {new_value}")
        return proxy
    
    def reset(self, proxy_id: str) -> Optional[CausalProxy]:
        """Reset proxy to original value"""
        proxy = self._proxies.get(proxy_id)
        if proxy:
            proxy.value = proxy.original_value
            proxy.is_modified = False
            logger.info(f"Reset proxy {proxy.name}")
        return proxy
    
    def get_modified(self) -> List[CausalProxy]:
        """Get all modified proxies"""
        return [p for p in self._proxies.values() if p.is_modified]


# ============================================================================
# RIPPLE EFFECT ENGINE
# ============================================================================

class RippleEffectEngine:
    """
    Visualize ripple effects.
    
    Per spec: Onde visuelle propagée vers les effets
    """
    
    def __init__(self, causal_graph: Dict[str, List[str]] = None):
        # Mock causal graph: source -> [targets]
        self._graph = causal_graph or {}
    
    def set_graph(self, graph: Dict[str, List[str]]) -> None:
        """Set causal graph"""
        self._graph = graph
    
    def compute_ripple(
        self,
        source_proxy_id: str,
        change_percent: float,
    ) -> RippleWave:
        """
        Compute ripple wave from source.
        
        Per spec: Couleur - Vert: positif, Rouge: négatif
        """
        affected = self._graph.get(source_proxy_id, [])
        
        # Determine color based on change direction
        if change_percent > 0:
            color = ImpactColor.GREEN
        elif change_percent < 0:
            color = ImpactColor.RED
        else:
            color = ImpactColor.YELLOW
        
        # Intensity = force causale
        intensity = min(1.0, abs(change_percent) / 100)
        
        wave = RippleWave(
            source_proxy=source_proxy_id,
            affected_proxies=affected,
            color=color,
            intensity=intensity,
        )
        
        logger.info(f"Ripple from {source_proxy_id}: {len(affected)} affected, {color.value}")
        return wave


# ============================================================================
# CAUSAL MAGNIFIER
# ============================================================================

@dataclass
class MagnifierView:
    """View from causal magnifier"""
    source_slot: str
    target_slot: str
    p_value: float
    stability: float
    agent_source: str  # L2/L3 agent


class CausalMagnifier:
    """
    Zoom into causal links.
    
    Per spec: Causal Magnifier - Affiche p-value, stabilité, agent source
    """
    
    def __init__(self, causal_metadata: Dict[str, Dict] = None):
        # Mock metadata: "source->target" -> {p_value, stability, agent}
        self._metadata = causal_metadata or {}
    
    def magnify(
        self,
        source_slot: str,
        target_slot: str,
    ) -> Optional[MagnifierView]:
        """Magnify a causal link"""
        key = f"{source_slot}->{target_slot}"
        meta = self._metadata.get(key, {})
        
        if not meta:
            # Default values
            meta = {
                "p_value": 0.05,
                "stability": 0.8,
                "agent": "L2-Analyst",
            }
        
        view = MagnifierView(
            source_slot=source_slot,
            target_slot=target_slot,
            p_value=meta.get("p_value", 0.05),
            stability=meta.get("stability", 0.8),
            agent_source=meta.get("agent", "L2-Analyst"),
        )
        
        logger.info(f"Magnified {key}: p={view.p_value}, stability={view.stability}")
        return view


# ============================================================================
# INTERVENTION SYSTEM
# ============================================================================

class InterventionSystem:
    """
    Main causal intervention system.
    
    Per spec: Intervention Sans Risque
    """
    
    def __init__(self):
        self.proxies = CausalProxyManager()
        self.ripple = RippleEffectEngine()
        self.magnifier = CausalMagnifier()
        
        self._drafts: List[InterventionDraft] = []
        self._render_mode = RenderMode.GHOST_REALITY
        self._time_horizon: int = 12  # months
    
    def set_render_mode(self, mode: RenderMode) -> None:
        """
        Set render mode.
        
        Per spec modes: Ghost Reality, Risk Heatmap, Causal Threads
        """
        self._render_mode = mode
        logger.info(f"Render mode: {mode.value}")
    
    def grab_and_slide(
        self,
        proxy_id: str,
        new_value: float,
    ) -> Tuple[CausalProxy, RippleWave]:
        """
        Grab & Slide interaction.
        
        Per spec: KPI ou ressource représenté par sphère/levier
        """
        # Grab
        proxy = self.proxies.grab(proxy_id)
        if not proxy:
            raise ValueError(f"Proxy {proxy_id} not found")
        
        # Compute change
        change_percent = ((new_value - proxy.original_value) / proxy.original_value * 100
                         if proxy.original_value != 0 else 0)
        
        # Slide
        self.proxies.slide(proxy_id, new_value)
        
        # Generate ripple
        wave = self.ripple.compute_ripple(proxy_id, change_percent)
        
        # Release
        self.proxies.release(proxy_id)
        
        return proxy, wave
    
    def snapshot(self, approver_id: str = "") -> List[InterventionDraft]:
        """
        Snapshot current state.
        
        Per spec: Snapshot (geste poing fermé) → Création Draft Artifact
        """
        drafts = []
        
        for proxy in self.proxies.get_modified():
            draft = InterventionDraft(
                draft_id=generate_id(),
                proxy_id=proxy.proxy_id,
                original_value=proxy.original_value,
                new_value=proxy.value,
                downstream_effects={},  # Would come from ripple
            )
            
            # OPA validation (mock)
            if approver_id:
                draft.opa_approved = True
                draft.approver_id = approver_id
            
            drafts.append(draft)
            self._drafts.append(draft)
        
        logger.info(f"Snapshot: {len(drafts)} drafts created")
        return drafts
    
    def scrub_time(self, months: int) -> Dict[str, Any]:
        """
        Time scrubbing.
        
        Per spec: Timeline circulaire au sol, Horizons: 6/12/24 mois
        """
        self._time_horizon = months
        
        return {
            "horizon_months": months,
            "projection_mode": "active",
        }
    
    def export_xr_pack(
        self,
        signer_id: str,
    ) -> XRPack:
        """
        Export signed XR pack.
        
        Per spec: Export XR Pack signé (V1.5+)
        """
        pack = XRPack(
            pack_id=generate_id(),
            session_id=generate_id(),
            interventions=self._drafts,
            read_only=True,
        )
        
        pack.signature = sign_xr_pack(pack, signer_id)
        
        logger.info(f"Exported XR pack: {pack.pack_id}")
        return pack
    
    def get_xr_manifest(self) -> Dict[str, Any]:
        """Get XR manifest"""
        return {
            "type": "causal_intervention",
            "render_mode": self._render_mode.value,
            "time_horizon": self._time_horizon,
            "proxies": [
                {
                    "id": p.proxy_id,
                    "name": p.name,
                    "value": p.value,
                    "original": p.original_value,
                    "modified": p.is_modified,
                    "shape": p.shape,
                    "position": p.position,
                }
                for p in self.proxies._proxies.values()
            ],
            "draft_count": len(self._drafts),
            "read_only": True,  # XR = espace de compréhension
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_intervention_system() -> InterventionSystem:
    """Create causal intervention system"""
    return InterventionSystem()
