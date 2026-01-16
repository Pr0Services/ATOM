"""
============================================================================
CHE·NU™ V69 — SCHOLAR MICRO-CONTRIBUTION LEDGER
============================================================================
Spec: GPT1/CHE-NU_SCH_MICRO_CONTRIBUTION_TRACKING.md

Objective: Reward all measurable contributions.

Mechanism (per spec):
- Ledger blockchain lié aux Artifacts
- Attribution de parts (Scholar Equity)
- Traçabilité immuable

Use cases: Ideas, critiques, data cleaning, replications.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
import logging
import hashlib
import json

from ..models import (
    MicroContribution,
    ScholarEquity,
    ContributionType,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CONTRIBUTION WEIGHTS
# ============================================================================

# Default equity weights by contribution type
CONTRIBUTION_WEIGHTS = {
    ContributionType.IDEA: 20.0,
    ContributionType.DATA: 15.0,
    ContributionType.CODE: 15.0,
    ContributionType.REVIEW: 10.0,
    ContributionType.REPLICATION: 12.0,
    ContributionType.CRITIQUE: 8.0,
    ContributionType.CLEANING: 8.0,
    ContributionType.ANNOTATION: 5.0,
    ContributionType.FUNDING: 5.0,
    ContributionType.MENTORSHIP: 7.0,
}


# ============================================================================
# LEDGER BLOCK
# ============================================================================

@dataclass
class LedgerBlock:
    """
    A block in the contribution ledger.
    
    Per spec: Ledger blockchain lié aux Artifacts
    """
    block_number: int
    timestamp: datetime
    contributions: List[str]  # Contribution IDs
    previous_hash: str
    block_hash: str = ""
    
    def compute_hash(self) -> str:
        """Compute block hash"""
        data = {
            "block_number": self.block_number,
            "timestamp": self.timestamp.isoformat(),
            "contributions": self.contributions,
            "previous_hash": self.previous_hash,
        }
        self.block_hash = compute_hash(data)
        return self.block_hash


# ============================================================================
# CONTRIBUTION LEDGER
# ============================================================================

class ContributionLedger:
    """
    Immutable ledger for tracking contributions.
    
    Per spec: Traçabilité immuable
    """
    
    def __init__(self):
        self._contributions: Dict[str, MicroContribution] = {}
        self._blocks: List[LedgerBlock] = []
        self._pending_contributions: List[str] = []
        
        # By artifact
        self._contributions_by_artifact: Dict[str, Set[str]] = {}
        
        # By contributor
        self._contributions_by_contributor: Dict[str, Set[str]] = {}
        
        # Genesis block
        genesis = LedgerBlock(
            block_number=0,
            timestamp=datetime.utcnow(),
            contributions=[],
            previous_hash="0" * 64,
        )
        genesis.compute_hash()
        self._blocks.append(genesis)
    
    def record_contribution(
        self,
        artifact_id: str,
        contributor_id: str,
        contribution_type: ContributionType,
        description: str,
    ) -> MicroContribution:
        """
        Record a new contribution.
        
        Per spec: Récompenser toutes les contributions mesurables
        """
        contribution = MicroContribution(
            contribution_id=generate_id(),
            artifact_id=artifact_id,
            contributor_id=contributor_id,
            contribution_type=contribution_type,
            description=description,
        )
        
        self._contributions[contribution.contribution_id] = contribution
        self._pending_contributions.append(contribution.contribution_id)
        
        # Index
        if artifact_id not in self._contributions_by_artifact:
            self._contributions_by_artifact[artifact_id] = set()
        self._contributions_by_artifact[artifact_id].add(contribution.contribution_id)
        
        if contributor_id not in self._contributions_by_contributor:
            self._contributions_by_contributor[contributor_id] = set()
        self._contributions_by_contributor[contributor_id].add(contribution.contribution_id)
        
        logger.info(
            f"Recorded contribution {contribution.contribution_id}: "
            f"{contributor_id} → {artifact_id} ({contribution_type.value})"
        )
        
        return contribution
    
    def commit_block(self) -> Optional[LedgerBlock]:
        """Commit pending contributions to a new block"""
        if not self._pending_contributions:
            return None
        
        previous = self._blocks[-1]
        
        block = LedgerBlock(
            block_number=len(self._blocks),
            timestamp=datetime.utcnow(),
            contributions=self._pending_contributions.copy(),
            previous_hash=previous.block_hash,
        )
        block.compute_hash()
        
        # Update contributions with block info
        for cid in self._pending_contributions:
            self._contributions[cid].ledger_hash = block.block_hash
            self._contributions[cid].block_number = block.block_number
        
        self._blocks.append(block)
        self._pending_contributions = []
        
        logger.info(f"Committed block {block.block_number} with {len(block.contributions)} contributions")
        return block
    
    def verify_chain(self) -> bool:
        """Verify the integrity of the ledger chain"""
        for i in range(1, len(self._blocks)):
            current = self._blocks[i]
            previous = self._blocks[i - 1]
            
            # Verify previous hash link
            if current.previous_hash != previous.block_hash:
                logger.error(f"Chain broken at block {i}")
                return False
            
            # Verify block hash
            expected_hash = current.compute_hash()
            if current.block_hash != expected_hash:
                logger.error(f"Invalid hash at block {i}")
                return False
        
        return True
    
    def get_contribution(self, contribution_id: str) -> Optional[MicroContribution]:
        """Get contribution by ID"""
        return self._contributions.get(contribution_id)
    
    def get_contributions_for_artifact(self, artifact_id: str) -> List[MicroContribution]:
        """Get all contributions for an artifact"""
        cids = self._contributions_by_artifact.get(artifact_id, set())
        return [self._contributions[cid] for cid in cids if cid in self._contributions]
    
    def get_contributions_by_contributor(self, contributor_id: str) -> List[MicroContribution]:
        """Get all contributions by a contributor"""
        cids = self._contributions_by_contributor.get(contributor_id, set())
        return [self._contributions[cid] for cid in cids if cid in self._contributions]
    
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get ledger statistics"""
        return {
            "total_blocks": len(self._blocks),
            "total_contributions": len(self._contributions),
            "pending_contributions": len(self._pending_contributions),
            "chain_valid": self.verify_chain(),
            "latest_block": self._blocks[-1].block_number if self._blocks else 0,
        }


# ============================================================================
# EQUITY CALCULATOR
# ============================================================================

class EquityCalculator:
    """
    Calculate equity distribution for artifacts.
    
    Per spec: Attribution de parts (Scholar Equity)
    """
    
    def __init__(self, weights: Dict[ContributionType, float] = None):
        self.weights = weights or CONTRIBUTION_WEIGHTS.copy()
    
    def calculate_equity(
        self,
        contributions: List[MicroContribution],
    ) -> ScholarEquity:
        """Calculate equity distribution from contributions"""
        if not contributions:
            return ScholarEquity(artifact_id="unknown")
        
        artifact_id = contributions[0].artifact_id
        
        # Calculate raw scores
        contributor_scores: Dict[str, float] = {}
        type_scores: Dict[str, float] = {}
        
        for contrib in contributions:
            weight = self.weights.get(contrib.contribution_type, 1.0)
            
            # Contributor score
            if contrib.contributor_id not in contributor_scores:
                contributor_scores[contrib.contributor_id] = 0
            contributor_scores[contrib.contributor_id] += weight
            
            # Type score
            type_key = contrib.contribution_type.value
            if type_key not in type_scores:
                type_scores[type_key] = 0
            type_scores[type_key] += weight
        
        # Convert to percentages
        total_score = sum(contributor_scores.values())
        
        equity_distribution = {}
        if total_score > 0:
            equity_distribution = {
                cid: (score / total_score) * 100
                for cid, score in contributor_scores.items()
            }
        
        equity_by_type = {}
        if total_score > 0:
            equity_by_type = {
                t: (score / total_score) * 100
                for t, score in type_scores.items()
            }
        
        # Create equity record
        equity = ScholarEquity(
            artifact_id=artifact_id,
            total_contributions=len(contributions),
            equity_distribution=equity_distribution,
            equity_by_type=equity_by_type,
        )
        
        # Compute root hash
        equity.ledger_root_hash = compute_hash({
            "artifact_id": artifact_id,
            "contributions": [c.contribution_id for c in contributions],
            "distribution": equity_distribution,
        })
        
        return equity
    
    def update_contribution_equity(
        self,
        contribution: MicroContribution,
        equity: ScholarEquity,
    ) -> None:
        """Update contribution with its equity share"""
        share = equity.equity_distribution.get(contribution.contributor_id, 0)
        contribution.equity_share = share


# ============================================================================
# CONTRIBUTION TRACKER
# ============================================================================

class ContributionTracker:
    """
    Main interface for contribution tracking.
    """
    
    def __init__(self):
        self.ledger = ContributionLedger()
        self.calculator = EquityCalculator()
        
        # Equity cache
        self._equity_cache: Dict[str, ScholarEquity] = {}
    
    def record(
        self,
        artifact_id: str,
        contributor_id: str,
        contribution_type: ContributionType,
        description: str,
    ) -> MicroContribution:
        """Record a contribution"""
        contrib = self.ledger.record_contribution(
            artifact_id=artifact_id,
            contributor_id=contributor_id,
            contribution_type=contribution_type,
            description=description,
        )
        
        # Invalidate equity cache
        if artifact_id in self._equity_cache:
            del self._equity_cache[artifact_id]
        
        return contrib
    
    def commit(self) -> Optional[LedgerBlock]:
        """Commit pending contributions"""
        return self.ledger.commit_block()
    
    def verify_contribution(
        self,
        contribution_id: str,
        verifier_id: str,
    ) -> bool:
        """Verify a contribution"""
        contrib = self.ledger.get_contribution(contribution_id)
        if not contrib:
            return False
        
        contrib.verified = True
        contrib.verified_by = verifier_id
        return True
    
    def get_equity(self, artifact_id: str) -> ScholarEquity:
        """Get equity distribution for an artifact"""
        if artifact_id in self._equity_cache:
            return self._equity_cache[artifact_id]
        
        contributions = self.ledger.get_contributions_for_artifact(artifact_id)
        equity = self.calculator.calculate_equity(contributions)
        
        # Update contributions with equity shares
        for contrib in contributions:
            self.calculator.update_contribution_equity(contrib, equity)
        
        self._equity_cache[artifact_id] = equity
        return equity
    
    def get_contributor_portfolio(
        self,
        contributor_id: str,
    ) -> Dict[str, Any]:
        """Get all contributions and equity for a contributor"""
        contributions = self.ledger.get_contributions_by_contributor(contributor_id)
        
        # Group by artifact
        by_artifact: Dict[str, List[MicroContribution]] = {}
        for c in contributions:
            if c.artifact_id not in by_artifact:
                by_artifact[c.artifact_id] = []
            by_artifact[c.artifact_id].append(c)
        
        # Calculate total equity
        total_equity = 0
        artifact_details = []
        
        for artifact_id, contribs in by_artifact.items():
            equity = self.get_equity(artifact_id)
            share = equity.equity_distribution.get(contributor_id, 0)
            total_equity += share
            
            artifact_details.append({
                "artifact_id": artifact_id,
                "contributions": len(contribs),
                "equity_share": share,
            })
        
        return {
            "contributor_id": contributor_id,
            "total_contributions": len(contributions),
            "total_equity": total_equity,
            "artifacts": artifact_details,
        }
    
    def export_ledger(self) -> Dict[str, Any]:
        """Export full ledger for audit"""
        return {
            "blocks": [
                {
                    "block_number": b.block_number,
                    "timestamp": b.timestamp.isoformat(),
                    "contributions": b.contributions,
                    "previous_hash": b.previous_hash,
                    "block_hash": b.block_hash,
                }
                for b in self.ledger._blocks
            ],
            "stats": self.ledger.get_chain_stats(),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_tracker() -> ContributionTracker:
    """Create a contribution tracker"""
    return ContributionTracker()


def create_ledger() -> ContributionLedger:
    """Create a contribution ledger"""
    return ContributionLedger()


def create_equity_calculator() -> EquityCalculator:
    """Create an equity calculator"""
    return EquityCalculator()
