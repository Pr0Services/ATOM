"""
============================================================================
CHE·NU™ V69 — SCHOLAR REPRODUCIBILITY PROTOCOL
============================================================================
Spec: GPT1/CHE-NU_SCH_REPRODUCIBILITY_PROTOCOL.md

Objective: Assign CHE·NU Verified score to each study.

Pipeline (per spec):
1. Ingestion (code + données synthétiques)
2. Re-run autonome (WorldEngine)
3. Comparaison des sorties
4. Score de reproductibilité

Outputs (per spec):
- Badge Verified
- Rapport d'écart
- Artifact signé

Impact: Eliminate fraud and calculation errors.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import hashlib
import json

from ..models import (
    ReproducibilityJob,
    ReproducibilityStatus,
    VerifiedBadge,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# BADGE LEVELS
# ============================================================================

BADGE_LEVELS = {
    "platinum": 0.95,  # >= 95% reproducibility
    "gold": 0.85,  # >= 85%
    "silver": 0.70,  # >= 70%
    "bronze": 0.50,  # >= 50%
}


def determine_badge_level(score: float) -> str:
    """Determine badge level from reproducibility score"""
    for level, threshold in sorted(BADGE_LEVELS.items(), key=lambda x: x[1], reverse=True):
        if score >= threshold:
            return level
    return "none"


# ============================================================================
# OUTPUT COMPARATOR
# ============================================================================

class OutputComparator:
    """
    Compare outputs between original and reproduced runs.
    
    Per spec: Comparaison des sorties
    """
    
    def __init__(
        self,
        numeric_tolerance: float = 0.001,
        string_exact: bool = True,
    ):
        self.numeric_tolerance = numeric_tolerance
        self.string_exact = string_exact
    
    def compare(
        self,
        original: Dict[str, Any],
        reproduced: Dict[str, Any],
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Compare two output dictionaries.
        
        Returns (match_percentage, discrepancies)
        """
        discrepancies = []
        total_fields = 0
        matching_fields = 0
        
        all_keys = set(original.keys()) | set(reproduced.keys())
        
        for key in all_keys:
            total_fields += 1
            
            orig_val = original.get(key)
            repr_val = reproduced.get(key)
            
            if key not in original:
                discrepancies.append({
                    "field": key,
                    "type": "missing_in_original",
                    "reproduced_value": repr_val,
                })
            elif key not in reproduced:
                discrepancies.append({
                    "field": key,
                    "type": "missing_in_reproduced",
                    "original_value": orig_val,
                })
            elif self._values_match(orig_val, repr_val):
                matching_fields += 1
            else:
                discrepancies.append({
                    "field": key,
                    "type": "value_mismatch",
                    "original_value": orig_val,
                    "reproduced_value": repr_val,
                    "difference": self._compute_difference(orig_val, repr_val),
                })
        
        match_percentage = matching_fields / total_fields if total_fields > 0 else 0
        return match_percentage, discrepancies
    
    def _values_match(self, orig: Any, repr: Any) -> bool:
        """Check if two values match"""
        if type(orig) != type(repr):
            return False
        
        if isinstance(orig, (int, float)) and isinstance(repr, (int, float)):
            if orig == 0 and repr == 0:
                return True
            relative_diff = abs(orig - repr) / max(abs(orig), abs(repr), 1)
            return relative_diff <= self.numeric_tolerance
        
        if isinstance(orig, str):
            if self.string_exact:
                return orig == repr
            return orig.strip().lower() == repr.strip().lower()
        
        if isinstance(orig, list):
            if len(orig) != len(repr):
                return False
            return all(self._values_match(o, r) for o, r in zip(orig, repr))
        
        if isinstance(orig, dict):
            if set(orig.keys()) != set(repr.keys()):
                return False
            return all(self._values_match(orig[k], repr[k]) for k in orig.keys())
        
        return orig == repr
    
    def _compute_difference(self, orig: Any, repr: Any) -> Any:
        """Compute difference between values"""
        if isinstance(orig, (int, float)) and isinstance(repr, (int, float)):
            return repr - orig
        return None


# ============================================================================
# REPRODUCIBILITY WORKER
# ============================================================================

class ReproducibilityWorker:
    """
    Worker for running reproducibility checks.
    
    Per spec: Worker de Validation Automatique
    """
    
    def __init__(
        self,
        executor: Callable[[str, str], Dict[str, Any]] = None,
    ):
        # Executor function: (code_ref, data_ref) -> output
        self._executor = executor or self._mock_executor
        self.comparator = OutputComparator()
    
    def _mock_executor(
        self,
        code_ref: str,
        data_ref: str,
    ) -> Dict[str, Any]:
        """Mock executor for testing"""
        # In production, this would run the actual code
        return {
            "result": 42,
            "metrics": [0.1, 0.2, 0.3],
            "status": "completed",
        }
    
    def run_job(
        self,
        job: ReproducibilityJob,
        original_output: Dict[str, Any],
    ) -> ReproducibilityJob:
        """
        Run reproducibility check.
        
        Per spec pipeline:
        1. Ingestion (code + données synthétiques)
        2. Re-run autonome (WorldEngine)
        3. Comparaison des sorties
        4. Score de reproductibilité
        """
        job.status = ReproducibilityStatus.RUNNING
        job.started_at = datetime.utcnow()
        
        try:
            # Step 2: Re-run
            reproduced_output = self._executor(job.code_ref, job.data_ref)
            
            # Step 3: Compare outputs
            match_pct, discrepancies = self.comparator.compare(
                original_output,
                reproduced_output,
            )
            
            # Step 4: Calculate score
            job.output_match_percentage = match_pct
            job.reproducibility_score = match_pct
            job.discrepancies = discrepancies
            
            # Determine status
            if match_pct >= 0.95:
                job.status = ReproducibilityStatus.PASSED
            elif match_pct >= 0.5:
                job.status = ReproducibilityStatus.PARTIAL
            else:
                job.status = ReproducibilityStatus.FAILED
            
        except Exception as e:
            job.status = ReproducibilityStatus.FAILED
            job.discrepancies = [{"error": str(e)}]
            job.reproducibility_score = 0
        
        job.completed_at = datetime.utcnow()
        
        logger.info(
            f"Job {job.job_id} completed: "
            f"score={job.reproducibility_score:.1%}, status={job.status.value}"
        )
        
        return job


# ============================================================================
# BADGE GENERATOR
# ============================================================================

class BadgeGenerator:
    """
    Generate verified badges for artifacts.
    
    Per spec outputs: Badge Verified
    """
    
    def __init__(self, signer: Callable[[str], str] = None):
        self._signer = signer or self._mock_sign
    
    def _mock_sign(self, data: str) -> str:
        """Mock signer for testing"""
        return compute_hash(f"signed:{data}")
    
    def generate_badge(
        self,
        artifact_id: str,
        reproducibility_score: float,
        report_ref: str = "",
    ) -> VerifiedBadge:
        """
        Generate verified badge.
        
        Per spec: Badge Verified, Rapport d'écart, Artifact signé
        """
        badge_level = determine_badge_level(reproducibility_score)
        
        badge = VerifiedBadge(
            badge_id=generate_id(),
            artifact_id=artifact_id,
            reproducibility_score=reproducibility_score,
            badge_level=badge_level,
            report_ref=report_ref,
        )
        
        # Sign the badge
        badge_data = json.dumps({
            "badge_id": badge.badge_id,
            "artifact_id": artifact_id,
            "score": reproducibility_score,
            "level": badge_level,
        }, sort_keys=True)
        
        badge.signature = self._signer(badge_data)
        
        logger.info(f"Generated {badge_level} badge for artifact {artifact_id}")
        return badge


# ============================================================================
# REPRODUCIBILITY PROTOCOL
# ============================================================================

class ReproducibilityProtocol:
    """
    Main protocol for reproducibility verification.
    """
    
    def __init__(
        self,
        executor: Callable = None,
        signer: Callable = None,
    ):
        self.worker = ReproducibilityWorker(executor)
        self.badge_gen = BadgeGenerator(signer)
        
        # Job storage
        self._jobs: Dict[str, ReproducibilityJob] = {}
        self._badges: Dict[str, VerifiedBadge] = {}
    
    def create_job(
        self,
        artifact_id: str,
        code_ref: str,
        data_ref: str,
    ) -> ReproducibilityJob:
        """Create a reproducibility job"""
        job = ReproducibilityJob(
            job_id=generate_id(),
            artifact_id=artifact_id,
            code_ref=code_ref,
            data_ref=data_ref,
        )
        
        self._jobs[job.job_id] = job
        logger.info(f"Created reproducibility job {job.job_id} for artifact {artifact_id}")
        return job
    
    def run_verification(
        self,
        job_id: str,
        original_output: Dict[str, Any],
    ) -> Tuple[ReproducibilityJob, Optional[VerifiedBadge]]:
        """Run verification and generate badge if passed"""
        job = self._jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        # Run the job
        job = self.worker.run_job(job, original_output)
        
        # Generate badge if passed or partial
        badge = None
        if job.status in [ReproducibilityStatus.PASSED, ReproducibilityStatus.PARTIAL]:
            report_ref = self._generate_report(job)
            badge = self.badge_gen.generate_badge(
                artifact_id=job.artifact_id,
                reproducibility_score=job.reproducibility_score,
                report_ref=report_ref,
            )
            self._badges[badge.badge_id] = badge
        
        return job, badge
    
    def _generate_report(self, job: ReproducibilityJob) -> str:
        """
        Generate discrepancy report.
        
        Per spec: Rapport d'écart
        """
        report = {
            "job_id": job.job_id,
            "artifact_id": job.artifact_id,
            "reproducibility_score": job.reproducibility_score,
            "output_match_percentage": job.output_match_percentage,
            "status": job.status.value,
            "discrepancies": job.discrepancies,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        }
        
        # In production, store report and return reference
        report_hash = compute_hash(report)
        return f"report:{report_hash}"
    
    def get_job(self, job_id: str) -> Optional[ReproducibilityJob]:
        """Get job by ID"""
        return self._jobs.get(job_id)
    
    def get_badge(self, badge_id: str) -> Optional[VerifiedBadge]:
        """Get badge by ID"""
        return self._badges.get(badge_id)
    
    def get_badge_for_artifact(self, artifact_id: str) -> Optional[VerifiedBadge]:
        """Get badge for an artifact"""
        for badge in self._badges.values():
            if badge.artifact_id == artifact_id:
                return badge
        return None
    
    def verify_badge(self, badge: VerifiedBadge) -> bool:
        """Verify badge signature"""
        badge_data = json.dumps({
            "badge_id": badge.badge_id,
            "artifact_id": badge.artifact_id,
            "score": badge.reproducibility_score,
            "level": badge.badge_level,
        }, sort_keys=True)
        
        expected_sig = self.badge_gen._signer(badge_data)
        return badge.signature == expected_sig
    
    def get_stats(self) -> Dict[str, Any]:
        """Get protocol statistics"""
        jobs = list(self._jobs.values())
        badges = list(self._badges.values())
        
        return {
            "total_jobs": len(jobs),
            "completed_jobs": sum(1 for j in jobs if j.status != ReproducibilityStatus.PENDING),
            "passed_jobs": sum(1 for j in jobs if j.status == ReproducibilityStatus.PASSED),
            "partial_jobs": sum(1 for j in jobs if j.status == ReproducibilityStatus.PARTIAL),
            "failed_jobs": sum(1 for j in jobs if j.status == ReproducibilityStatus.FAILED),
            "total_badges": len(badges),
            "badge_distribution": {
                level: sum(1 for b in badges if b.badge_level == level)
                for level in ["platinum", "gold", "silver", "bronze"]
            },
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_protocol() -> ReproducibilityProtocol:
    """Create reproducibility protocol"""
    return ReproducibilityProtocol()


def create_worker() -> ReproducibilityWorker:
    """Create reproducibility worker"""
    return ReproducibilityWorker()


def create_badge_generator() -> BadgeGenerator:
    """Create badge generator"""
    return BadgeGenerator()
