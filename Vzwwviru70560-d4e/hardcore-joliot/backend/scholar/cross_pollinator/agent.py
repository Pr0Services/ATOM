"""
============================================================================
CHE·NU™ V69 — SCHOLAR CROSS-POLLINATION AGENT (L3)
============================================================================
Spec: GPT1/CHE-NU_SCH_AGENT_CROSS_POLLINATOR_LOGIC.md

Role: Scan Artifacts and notify useful matches.

Logic (per spec):
- Analyse causale
- Mapping via Interoperability Matrix
- Notifications contextualisées

Impact: Création de task-forces spontanées
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import logging

from ..models import (
    CrossPollinationMatch,
    TaskForce,
    CausalNode,
    generate_id,
)

logger = logging.getLogger(__name__)


# ============================================================================
# INTEROPERABILITY MATRIX
# ============================================================================

# Domain similarity matrix (simplified)
DOMAIN_INTEROPERABILITY = {
    ("biology", "engineering"): 0.7,
    ("biology", "chemistry"): 0.9,
    ("biology", "medicine"): 0.95,
    ("physics", "engineering"): 0.85,
    ("physics", "materials"): 0.8,
    ("chemistry", "materials"): 0.85,
    ("computer_science", "mathematics"): 0.9,
    ("computer_science", "engineering"): 0.75,
    ("economics", "sociology"): 0.7,
    ("psychology", "neuroscience"): 0.85,
    ("climate", "ecology"): 0.9,
    ("energy", "engineering"): 0.8,
}


def get_domain_interoperability(domain_a: str, domain_b: str) -> float:
    """Get interoperability score between two domains"""
    if domain_a == domain_b:
        return 1.0
    
    key = tuple(sorted([domain_a, domain_b]))
    score = DOMAIN_INTEROPERABILITY.get(key, 0.3)
    return score


# ============================================================================
# SIMILARITY TYPES
# ============================================================================

class SimilarityType:
    """Types of similarity for cross-pollination"""
    CAUSAL = "causal"  # Similar causal structures
    METHODOLOGICAL = "methodological"  # Similar methods
    STRUCTURAL = "structural"  # Similar data structures
    PATTERN = "pattern"  # Similar patterns/equations
    GOAL = "goal"  # Similar objectives


# ============================================================================
# NOTIFICATION
# ============================================================================

@dataclass
class CrossPollinationNotification:
    """Notification for cross-pollination match"""
    notification_id: str
    match_id: str
    recipient_ids: List[str]
    
    # Content
    title: str
    summary: str
    relevance_score: float
    
    # Status
    sent: bool = False
    sent_at: Optional[datetime] = None
    read_by: List[str] = field(default_factory=list)
    
    # Actions taken
    task_force_created: bool = False


# ============================================================================
# CROSS-POLLINATOR SCANNER
# ============================================================================

class CrossPollinatorScanner:
    """
    Scanner for finding cross-pollination opportunities.
    
    Per spec: Scanner les Artifacts et notifier des correspondances utiles
    """
    
    def __init__(
        self,
        min_similarity: float = 0.6,
        min_interoperability: float = 0.5,
    ):
        self.min_similarity = min_similarity
        self.min_interoperability = min_interoperability
    
    def scan_for_matches(
        self,
        artifacts: List[Dict[str, Any]],
    ) -> List[CrossPollinationMatch]:
        """
        Scan artifacts for cross-pollination opportunities.
        
        Per spec: Analyse causale + Mapping via Interoperability Matrix
        """
        matches = []
        
        # Compare all pairs
        for i, art_a in enumerate(artifacts):
            for art_b in artifacts[i+1:]:
                # Skip same domain (we want cross-pollination)
                if art_a.get("domain") == art_b.get("domain"):
                    continue
                
                # Check interoperability
                interop = get_domain_interoperability(
                    art_a.get("domain", ""),
                    art_b.get("domain", ""),
                )
                
                if interop < self.min_interoperability:
                    continue
                
                # Compute similarity
                similarity, sim_type = self._compute_similarity(art_a, art_b)
                
                if similarity >= self.min_similarity:
                    match = CrossPollinationMatch(
                        match_id=generate_id(),
                        artifact_a=art_a.get("id", ""),
                        artifact_b=art_b.get("id", ""),
                        domain_a=art_a.get("domain", ""),
                        domain_b=art_b.get("domain", ""),
                        similarity_type=sim_type,
                        similarity_score=similarity * interop,
                    )
                    matches.append(match)
        
        # Sort by score
        matches.sort(key=lambda m: m.similarity_score, reverse=True)
        
        logger.info(f"Found {len(matches)} cross-pollination matches")
        return matches
    
    def _compute_similarity(
        self,
        art_a: Dict[str, Any],
        art_b: Dict[str, Any],
    ) -> Tuple[float, str]:
        """Compute similarity between two artifacts"""
        scores = {}
        
        # Keyword overlap
        keywords_a = set(art_a.get("keywords", []))
        keywords_b = set(art_b.get("keywords", []))
        if keywords_a or keywords_b:
            keyword_sim = len(keywords_a & keywords_b) / max(len(keywords_a | keywords_b), 1)
            scores[SimilarityType.PATTERN] = keyword_sim
        
        # Method similarity
        methods_a = set(art_a.get("methods", []))
        methods_b = set(art_b.get("methods", []))
        if methods_a or methods_b:
            method_sim = len(methods_a & methods_b) / max(len(methods_a | methods_b), 1)
            scores[SimilarityType.METHODOLOGICAL] = method_sim
        
        # Goal similarity (simple text comparison)
        goal_a = art_a.get("goal", "").lower()
        goal_b = art_b.get("goal", "").lower()
        if goal_a and goal_b:
            words_a = set(goal_a.split())
            words_b = set(goal_b.split())
            goal_sim = len(words_a & words_b) / max(len(words_a | words_b), 1)
            scores[SimilarityType.GOAL] = goal_sim
        
        if not scores:
            return 0.0, SimilarityType.STRUCTURAL
        
        # Return best match
        best_type = max(scores.keys(), key=lambda k: scores[k])
        return scores[best_type], best_type


# ============================================================================
# NOTIFICATION GENERATOR
# ============================================================================

class NotificationGenerator:
    """
    Generate notifications for cross-pollination matches.
    
    Per spec: Notifications contextualisées
    """
    
    def generate_notification(
        self,
        match: CrossPollinationMatch,
        authors_a: List[str],
        authors_b: List[str],
    ) -> CrossPollinationNotification:
        """Generate notification for a match"""
        title = f"Cross-Domain Discovery: {match.domain_a} ↔ {match.domain_b}"
        
        summary = (
            f"A potential connection was found between work in {match.domain_a} "
            f"and {match.domain_b}. The similarity type is {match.similarity_type} "
            f"with a score of {match.similarity_score:.1%}. "
            f"Consider forming a task force to explore this connection."
        )
        
        return CrossPollinationNotification(
            notification_id=generate_id(),
            match_id=match.match_id,
            recipient_ids=list(set(authors_a + authors_b)),
            title=title,
            summary=summary,
            relevance_score=match.similarity_score,
        )


# ============================================================================
# TASK FORCE MANAGER
# ============================================================================

class TaskForceManager:
    """
    Manage task forces created from cross-pollination.
    
    Per spec: Création de task-forces spontanées
    """
    
    def __init__(self):
        self._task_forces: Dict[str, TaskForce] = {}
    
    def create_task_force(
        self,
        match: CrossPollinationMatch,
        proposed_members: List[str],
    ) -> TaskForce:
        """Create a task force from a match"""
        task_force = TaskForce(
            task_force_id=generate_id(),
            name=f"TF: {match.domain_a} × {match.domain_b}",
            match_id=match.match_id,
            members=proposed_members,
            domains=[match.domain_a, match.domain_b],
            status="proposed",
        )
        
        self._task_forces[task_force.task_force_id] = task_force
        match.task_force_created = True
        
        logger.info(f"Created task force {task_force.task_force_id}")
        return task_force
    
    def activate_task_force(self, task_force_id: str) -> bool:
        """Activate a proposed task force"""
        tf = self._task_forces.get(task_force_id)
        if tf and tf.status == "proposed":
            tf.status = "active"
            return True
        return False
    
    def complete_task_force(self, task_force_id: str) -> bool:
        """Mark task force as completed"""
        tf = self._task_forces.get(task_force_id)
        if tf and tf.status == "active":
            tf.status = "completed"
            return True
        return False
    
    def get_task_force(self, task_force_id: str) -> Optional[TaskForce]:
        """Get task force by ID"""
        return self._task_forces.get(task_force_id)
    
    def get_active_task_forces(self) -> List[TaskForce]:
        """Get all active task forces"""
        return [tf for tf in self._task_forces.values() if tf.status == "active"]


# ============================================================================
# CROSS-POLLINATOR AGENT
# ============================================================================

class CrossPollinatorAgent:
    """
    L3 Agent for cross-pollination.
    
    Per spec: Agent level L3
    """
    
    def __init__(self):
        self.scanner = CrossPollinatorScanner()
        self.notifier = NotificationGenerator()
        self.task_force_manager = TaskForceManager()
        
        # Stored matches and notifications
        self._matches: Dict[str, CrossPollinationMatch] = {}
        self._notifications: Dict[str, CrossPollinationNotification] = {}
    
    def process_artifacts(
        self,
        artifacts: List[Dict[str, Any]],
        author_map: Dict[str, List[str]] = None,  # artifact_id → author_ids
    ) -> List[CrossPollinationNotification]:
        """
        Process artifacts and generate notifications.
        
        Full pipeline per spec:
        1. Analyse causale
        2. Mapping via Interoperability Matrix
        3. Notifications contextualisées
        """
        author_map = author_map or {}
        
        # Step 1-2: Scan for matches
        matches = self.scanner.scan_for_matches(artifacts)
        
        # Store matches
        for match in matches:
            self._matches[match.match_id] = match
        
        # Step 3: Generate notifications
        notifications = []
        for match in matches:
            authors_a = author_map.get(match.artifact_a, [])
            authors_b = author_map.get(match.artifact_b, [])
            
            notif = self.notifier.generate_notification(match, authors_a, authors_b)
            notifications.append(notif)
            self._notifications[notif.notification_id] = notif
        
        logger.info(f"Generated {len(notifications)} cross-pollination notifications")
        return notifications
    
    def create_task_force_from_match(
        self,
        match_id: str,
        members: List[str],
    ) -> Optional[TaskForce]:
        """Create task force from a match"""
        match = self._matches.get(match_id)
        if not match:
            return None
        
        return self.task_force_manager.create_task_force(match, members)
    
    def get_matches_for_domain(self, domain: str) -> List[CrossPollinationMatch]:
        """Get all matches involving a domain"""
        return [
            m for m in self._matches.values()
            if m.domain_a == domain or m.domain_b == domain
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        matches = list(self._matches.values())
        notifications = list(self._notifications.values())
        task_forces = list(self.task_force_manager._task_forces.values())
        
        return {
            "total_matches": len(matches),
            "total_notifications": len(notifications),
            "notifications_sent": sum(1 for n in notifications if n.sent),
            "total_task_forces": len(task_forces),
            "active_task_forces": sum(1 for tf in task_forces if tf.status == "active"),
            "domain_pairs": list(set(
                tuple(sorted([m.domain_a, m.domain_b])) for m in matches
            )),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_cross_pollinator() -> CrossPollinatorAgent:
    """Create cross-pollinator agent"""
    return CrossPollinatorAgent()


def create_scanner(
    min_similarity: float = 0.6,
) -> CrossPollinatorScanner:
    """Create cross-pollinator scanner"""
    return CrossPollinatorScanner(min_similarity)


def create_task_force_manager() -> TaskForceManager:
    """Create task force manager"""
    return TaskForceManager()
