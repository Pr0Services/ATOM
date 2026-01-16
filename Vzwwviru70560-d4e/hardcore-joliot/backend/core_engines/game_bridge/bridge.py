"""
============================================================================
CHE·NU™ V69 — WORLD TO GAME LOGIC BRIDGE
============================================================================
Spec: GPT1/CHE-NU_WORLD_TO_GAME_LOGIC_BRIDGE.md

Objective: Map serious WorldEngine data to game mechanics.

Mapping Examples:
- Budget → Points / Credits
- KPI → Stability bars
- Causal Links → Bonus / Penalties
- P-Value → Fog of War

Governance: No mapping without validation, OPA filters abusive mechanics
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    Slot,
    WorldState,
    CausalDAG,
    GameMapping,
    GameMechanicType,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# MAPPING RULES
# ============================================================================

@dataclass
class MappingRule:
    """A rule for mapping simulation data to game mechanics"""
    rule_id: str
    name: str
    
    # Source pattern
    source_pattern: str  # regex or keyword
    
    # Target mechanic
    target_mechanic: GameMechanicType
    
    # Transform
    scale_factor: float = 1.0
    offset: float = 0.0
    min_value: float = 0.0
    max_value: float = 100.0
    
    # Validation
    validated: bool = False


# ============================================================================
# GAME BRIDGE
# ============================================================================

class WorldToGameBridge:
    """
    Bridge between WorldEngine and game mechanics.
    
    Per spec: Mapper les données sérieuses vers des mécaniques de jeu
    """
    
    # Default mappings
    DEFAULT_MAPPINGS = {
        "budget": (GameMechanicType.POINTS, 1.0, 0.0),
        "cost": (GameMechanicType.POINTS, -1.0, 0.0),
        "health": (GameMechanicType.HEALTH_BAR, 1.0, 0.0),
        "stability": (GameMechanicType.HEALTH_BAR, 1.0, 0.0),
        "kpi": (GameMechanicType.HEALTH_BAR, 100.0, 0.0),
        "bonus": (GameMechanicType.BONUS, 1.0, 0.0),
        "penalty": (GameMechanicType.PENALTY, 1.0, 0.0),
        "risk": (GameMechanicType.PENALTY, 1.0, 0.0),
        "uncertainty": (GameMechanicType.FOG_OF_WAR, 1.0, 0.0),
        "p_value": (GameMechanicType.FOG_OF_WAR, 100.0, 0.0),  # Higher p-value = more fog
    }
    
    def __init__(self):
        self._mappings: Dict[str, GameMapping] = {}
        self._rules: Dict[str, MappingRule] = {}
        self._validated_mappings: set = set()
    
    def register_mapping(
        self,
        slot_id: str,
        mechanic_type: GameMechanicType,
        mechanic_name: str = "",
        scale: float = 1.0,
        offset: float = 0.0,
    ) -> GameMapping:
        """Register a mapping from slot to game mechanic"""
        mapping = GameMapping(
            mapping_id=generate_id(),
            slot_id=slot_id,
            mechanic_type=mechanic_type,
            mechanic_name=mechanic_name or f"{mechanic_type.value}_{slot_id}",
            scale_factor=scale,
            offset=offset,
        )
        
        self._mappings[slot_id] = mapping
        return mapping
    
    def auto_map(self, slot: Slot) -> Optional[GameMapping]:
        """
        Automatically map a slot based on its name.
        
        Per spec examples: Budget → Points, KPI → Barres
        """
        slot_lower = slot.name.lower()
        
        for keyword, (mechanic, scale, offset) in self.DEFAULT_MAPPINGS.items():
            if keyword in slot_lower:
                return self.register_mapping(
                    slot.slot_id,
                    mechanic,
                    f"{slot.name}_{mechanic.value}",
                    scale,
                    offset,
                )
        
        # Default to points
        return self.register_mapping(
            slot.slot_id,
            GameMechanicType.POINTS,
            f"{slot.name}_points",
        )
    
    def validate_mapping(
        self,
        mapping_id: str,
        validator_id: str,
    ) -> bool:
        """
        Validate a mapping.
        
        Per spec: Aucun mapping sans validation
        """
        for slot_id, mapping in self._mappings.items():
            if mapping.mapping_id == mapping_id:
                mapping.validated = True
                self._validated_mappings.add(mapping_id)
                logger.info(f"Mapping {mapping_id} validated by {validator_id}")
                return True
        
        return False
    
    def transform(
        self,
        slot: Slot,
    ) -> Dict[str, Any]:
        """Transform slot value to game mechanic value"""
        mapping = self._mappings.get(slot.slot_id)
        
        if not mapping:
            # Auto-map if not registered
            mapping = self.auto_map(slot)
        
        # Apply transform
        game_value = slot.value * mapping.scale_factor + mapping.offset
        
        return {
            "slot_id": slot.slot_id,
            "slot_name": slot.name,
            "slot_value": slot.value,
            "mechanic_type": mapping.mechanic_type.value,
            "mechanic_name": mapping.mechanic_name,
            "game_value": game_value,
            "validated": mapping.validated,
        }
    
    def transform_state(
        self,
        state: WorldState,
    ) -> Dict[str, Any]:
        """Transform entire world state to game state"""
        game_state = {
            "state_id": state.state_id,
            "sim_time": state.sim_time,
            "mechanics": {},
        }
        
        for slot_name, slot in state.slots.items():
            transformed = self.transform(slot)
            mechanic_type = transformed["mechanic_type"]
            
            if mechanic_type not in game_state["mechanics"]:
                game_state["mechanics"][mechanic_type] = []
            
            game_state["mechanics"][mechanic_type].append(transformed)
        
        return game_state
    
    def map_causal_links(
        self,
        dag: CausalDAG,
    ) -> List[Dict[str, Any]]:
        """
        Map causal links to bonuses/penalties.
        
        Per spec: Causal Links → Bonus / pénalités
        """
        game_links = []
        
        for edge in dag.edges:
            if edge.strength > 0:
                link_type = "bonus"
                effect_value = edge.strength * 10  # Scale to game value
            else:
                link_type = "penalty"
                effect_value = abs(edge.strength) * 10
            
            game_links.append({
                "source": edge.source_slot,
                "target": edge.target_slot,
                "link_type": link_type,
                "effect_value": effect_value,
                "strength": edge.strength,
            })
        
        return game_links
    
    def apply_fog_of_war(
        self,
        slot: Slot,
        p_value: float,
    ) -> Dict[str, Any]:
        """
        Apply fog of war based on p-value.
        
        Per spec: P-Value → Brouillard de guerre
        """
        # Higher p-value = less certain = more fog
        fog_level = min(1.0, p_value)  # 0 = no fog, 1 = full fog
        
        # Obscure the value based on fog
        if fog_level > 0.5:
            visible_value = "???"
            confidence = "low"
        elif fog_level > 0.2:
            visible_value = f"~{slot.value:.0f}"
            confidence = "medium"
        else:
            visible_value = f"{slot.value:.1f}"
            confidence = "high"
        
        return {
            "slot_id": slot.slot_id,
            "slot_name": slot.name,
            "visible_value": visible_value,
            "true_value": slot.value,
            "fog_level": fog_level,
            "confidence": confidence,
        }
    
    def generate_game_manifest(
        self,
        state: WorldState,
        dag: Optional[CausalDAG] = None,
    ) -> Dict[str, Any]:
        """Generate complete game manifest from simulation"""
        manifest = {
            "manifest_id": generate_id(),
            "source_state": state.state_id,
            "sim_time": state.sim_time,
            "mechanics": self.transform_state(state)["mechanics"],
        }
        
        if dag:
            manifest["causal_links"] = self.map_causal_links(dag)
        
        # Sign manifest
        manifest["signature"] = sign_artifact({
            "manifest_id": manifest["manifest_id"],
            "state_id": state.state_id,
        }, "game_bridge")
        
        return manifest


# ============================================================================
# OPA FILTER
# ============================================================================

class MechanicFilter:
    """
    Filter for abusive game mechanics.
    
    Per spec: OPA filtre les mécaniques abusives
    """
    
    # Blocked mechanics patterns
    BLOCKED_PATTERNS = [
        ("pay_to_win", "instant_win"),
        ("gambling", "slot_machine"),
        ("addiction", "infinite_loop"),
    ]
    
    def is_allowed(
        self,
        mapping: GameMapping,
    ) -> Tuple[bool, str]:
        """Check if mapping is allowed"""
        name_lower = mapping.mechanic_name.lower()
        
        for pattern_a, pattern_b in self.BLOCKED_PATTERNS:
            if pattern_a in name_lower or pattern_b in name_lower:
                return False, f"Blocked mechanic pattern: {pattern_a}/{pattern_b}"
        
        return True, ""
    
    def filter_mappings(
        self,
        mappings: List[GameMapping],
    ) -> List[GameMapping]:
        """Filter out blocked mappings"""
        return [m for m in mappings if self.is_allowed(m)[0]]


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_bridge() -> WorldToGameBridge:
    """Create world to game bridge"""
    return WorldToGameBridge()


def create_filter() -> MechanicFilter:
    """Create mechanic filter"""
    return MechanicFilter()
