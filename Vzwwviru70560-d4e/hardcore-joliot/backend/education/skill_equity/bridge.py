"""
============================================================================
CHE·NU™ V69 — EDUCATION SKILL TO EQUITY BRIDGE
============================================================================
Spec: GPT1/CHE-NU_EDU_SKILL_TO_EQUITY_BRIDGE.md

Objective: Connect learning to local economic reality, without automating
human decision.

Principle: Proven competence → access to complex tasks → better pay → equity

The bridge is an ELIGIBILITY mechanism (not forced assignment).
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from ..models import (
    NanoCertification,
    EligibilityRule,
    EligibilityTier,
    EligibilityProof,
    TaskEquityOffer,
    SkillCategory,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TIER DEFINITIONS
# ============================================================================

TIER_EQUITY_RATES = {
    EligibilityTier.TIER_0: 0.0,  # Observation (0 equity)
    EligibilityTier.TIER_1: 0.05,  # Supervised (5% equity)
    EligibilityTier.TIER_2: 0.15,  # Autonomous (15% equity)
    EligibilityTier.TIER_3: 0.30,  # Premium (30% equity)
}

TIER_SALARY_MULTIPLIERS = {
    EligibilityTier.TIER_0: 0.5,
    EligibilityTier.TIER_1: 1.0,
    EligibilityTier.TIER_2: 1.5,
    EligibilityTier.TIER_3: 2.5,
}


# ============================================================================
# ELIGIBILITY EVALUATOR
# ============================================================================

class EligibilityEvaluator:
    """
    Evaluate user eligibility for tasks.
    
    Per spec: Règles d'éligibilité
    """
    
    def __init__(self):
        self._rules: Dict[str, EligibilityRule] = {}
        self._rules_by_family: Dict[str, List[str]] = {}  # family → rule_ids
    
    def add_rule(self, rule: EligibilityRule) -> str:
        """Add eligibility rule"""
        self._rules[rule.rule_id] = rule
        
        if rule.task_family not in self._rules_by_family:
            self._rules_by_family[rule.task_family] = []
        self._rules_by_family[rule.task_family].append(rule.rule_id)
        
        return rule.rule_id
    
    def evaluate(
        self,
        user_certs: List[str],
        user_trust_score: float,
        user_simulations_passed: int,
        user_xr_exams_passed: int,
        task_family: str,
    ) -> Tuple[bool, Optional[EligibilityTier], List[str]]:
        """
        Evaluate eligibility.
        
        Returns (is_eligible, tier, unmet_requirements)
        """
        rule_ids = self._rules_by_family.get(task_family, [])
        
        best_tier = None
        eligible = False
        unmet = []
        
        for rule_id in rule_ids:
            rule = self._rules[rule_id]
            
            # Check requirements
            requirements_met = True
            rule_unmet = []
            
            # Check certs
            for cert_id in rule.required_certs:
                if cert_id not in user_certs:
                    requirements_met = False
                    rule_unmet.append(f"missing_cert:{cert_id}")
            
            # Check trust score
            if user_trust_score < rule.min_trust_score:
                requirements_met = False
                rule_unmet.append(f"trust_score_too_low:{user_trust_score}<{rule.min_trust_score}")
            
            # Check simulations
            if user_simulations_passed < rule.required_simulations:
                requirements_met = False
                rule_unmet.append(f"simulations:{user_simulations_passed}<{rule.required_simulations}")
            
            # Check XR exams
            if user_xr_exams_passed < rule.required_xr_exams:
                requirements_met = False
                rule_unmet.append(f"xr_exams:{user_xr_exams_passed}<{rule.required_xr_exams}")
            
            if requirements_met:
                eligible = True
                if best_tier is None or rule.tier.value > best_tier.value:
                    best_tier = rule.tier
            else:
                unmet.extend(rule_unmet)
        
        return eligible, best_tier, unmet
    
    def get_rules_for_family(self, task_family: str) -> List[EligibilityRule]:
        """Get rules for a task family"""
        rule_ids = self._rules_by_family.get(task_family, [])
        return [self._rules[rid] for rid in rule_ids]


# ============================================================================
# PROOF GENERATOR
# ============================================================================

class ProofGenerator:
    """
    Generate eligibility proofs.
    
    Per spec artifact: ELIGIBILITY_PROOF.json
    """
    
    def generate(
        self,
        user_id: str,
        certs: List[str],
        trust_score: float,
        assessment_proofs: List[str],
    ) -> EligibilityProof:
        """Generate eligibility proof"""
        proof = EligibilityProof(
            proof_id=generate_id(),
            user_id=user_id,
            certs=certs,
            trust_score_snapshot=trust_score,
            assessment_proof_links=assessment_proofs,
        )
        
        # Sign proof
        proof.signature = sign_artifact({
            "proof_id": proof.proof_id,
            "user_id": user_id,
            "certs": certs,
            "trust_score": trust_score,
        }, "eligibility_authority")
        
        return proof


# ============================================================================
# EQUITY CALCULATOR
# ============================================================================

class EquityCalculator:
    """
    Calculate equity and salary splits.
    
    Per spec: Le module calcule sur PREUVE, pas sur promesse.
    
    Inputs: complexité tâche, risque, rareté compétence, Trust Score
    Output: salary_split, equity_split, confidence
    """
    
    def calculate(
        self,
        tier: EligibilityTier,
        task_complexity: float,  # 0-1
        task_risk: SkillCategory,
        skill_scarcity: float,  # 0-1, higher = rarer
        trust_score: float,  # 0-1
        base_salary: float = 1000.0,
    ) -> Dict[str, Any]:
        """Calculate splits"""
        # Base rates from tier
        base_equity_rate = TIER_EQUITY_RATES[tier]
        salary_multiplier = TIER_SALARY_MULTIPLIERS[tier]
        
        # Adjust for complexity
        complexity_bonus = task_complexity * 0.2
        
        # Adjust for scarcity
        scarcity_bonus = skill_scarcity * 0.15
        
        # Risk adjustment (higher risk = lower equity offered)
        risk_factor = {
            SkillCategory.CATEGORY_A: 1.0,
            SkillCategory.CATEGORY_B: 0.9,
            SkillCategory.CATEGORY_C: 0.8,
        }.get(task_risk, 1.0)
        
        # Final equity rate
        equity_rate = (base_equity_rate + complexity_bonus + scarcity_bonus) * risk_factor
        equity_rate = min(0.5, equity_rate)  # Cap at 50%
        
        # Salary calculation
        salary = base_salary * salary_multiplier * (1 + task_complexity)
        
        # Confidence based on trust score
        confidence = 0.5 + (trust_score * 0.4) + (1 - skill_scarcity) * 0.1
        confidence = min(1.0, confidence)
        
        return {
            "salary_split": salary,
            "equity_split": equity_rate,
            "confidence": confidence,
            "tier": tier.value,
            "factors": {
                "base_equity_rate": base_equity_rate,
                "complexity_bonus": complexity_bonus,
                "scarcity_bonus": scarcity_bonus,
                "risk_factor": risk_factor,
            },
        }


# ============================================================================
# TASK OFFER GENERATOR
# ============================================================================

class TaskOfferGenerator:
    """
    Generate task equity offers.
    
    Per spec artifact: TASK_EQUITY_OFFER.json
    """
    
    def __init__(self):
        self.equity_calc = EquityCalculator()
        self._offers: Dict[str, TaskEquityOffer] = {}
    
    def generate_offer(
        self,
        task_id: str,
        user_id: str,
        tier: EligibilityTier,
        task_complexity: float,
        task_risk: SkillCategory,
        skill_scarcity: float,
        trust_score: float,
        base_salary: float = 1000.0,
        vesting_months: int = 12,
    ) -> TaskEquityOffer:
        """Generate task equity offer"""
        # Calculate splits
        calc = self.equity_calc.calculate(
            tier=tier,
            task_complexity=task_complexity,
            task_risk=task_risk,
            skill_scarcity=skill_scarcity,
            trust_score=trust_score,
            base_salary=base_salary,
        )
        
        offer = TaskEquityOffer(
            offer_id=generate_id(),
            task_id=task_id,
            user_id=user_id,
            salary_split=calc["salary_split"],
            equity_split=calc["equity_split"],
            vesting_months=vesting_months,
            vesting_rules={
                "cliff_months": 3,
                "schedule": "monthly",
                "conditions": ["task_completion", "quality_threshold"],
            },
            opa_compliant=True,
        )
        
        # Sign offer
        offer.signature = sign_artifact({
            "offer_id": offer.offer_id,
            "task_id": task_id,
            "user_id": user_id,
            "salary": offer.salary_split,
            "equity": offer.equity_split,
        }, "task_equity_authority")
        
        self._offers[offer.offer_id] = offer
        return offer
    
    def accept_offer(self, offer_id: str) -> bool:
        """User accepts offer"""
        offer = self._offers.get(offer_id)
        if offer and offer.status == "pending":
            offer.status = "accepted"
            return True
        return False
    
    def reject_offer(self, offer_id: str) -> bool:
        """User rejects offer"""
        offer = self._offers.get(offer_id)
        if offer and offer.status == "pending":
            offer.status = "rejected"
            return True
        return False
    
    def get_offer(self, offer_id: str) -> Optional[TaskEquityOffer]:
        """Get offer by ID"""
        return self._offers.get(offer_id)


# ============================================================================
# SKILL TO EQUITY BRIDGE
# ============================================================================

class SkillToEquityBridge:
    """
    Main bridge connecting skills to economic opportunities.
    
    Per spec UX:
    1. User completes pathway
    2. Receives badge + proof
    3. UI shows "New opportunities unlocked"
    4. User CHOOSES a mission
    5. Synthetic contract generated
    """
    
    def __init__(self):
        self.evaluator = EligibilityEvaluator()
        self.proof_gen = ProofGenerator()
        self.offer_gen = TaskOfferGenerator()
        
        # User data
        self._user_certs: Dict[str, Set[str]] = {}  # user_id → cert_ids
        self._user_trust_scores: Dict[str, float] = {}
        self._user_simulations: Dict[str, int] = {}
        self._user_xr_exams: Dict[str, int] = {}
        
        # Proofs
        self._proofs: Dict[str, EligibilityProof] = {}
    
    def register_certification(
        self,
        user_id: str,
        cert_id: str,
    ) -> None:
        """Register user certification"""
        if user_id not in self._user_certs:
            self._user_certs[user_id] = set()
        self._user_certs[user_id].add(cert_id)
    
    def update_trust_score(
        self,
        user_id: str,
        score: float,
    ) -> None:
        """Update user trust score"""
        self._user_trust_scores[user_id] = score
    
    def record_simulation_pass(self, user_id: str) -> None:
        """Record passed simulation"""
        self._user_simulations[user_id] = self._user_simulations.get(user_id, 0) + 1
    
    def record_xr_exam_pass(self, user_id: str) -> None:
        """Record passed XR exam"""
        self._user_xr_exams[user_id] = self._user_xr_exams.get(user_id, 0) + 1
    
    def check_eligibility(
        self,
        user_id: str,
        task_family: str,
    ) -> Dict[str, Any]:
        """
        Check if user is eligible for a task family.
        
        Per spec: mécanisme d'éligibilité (pas un système d'affectation forcée)
        """
        certs = list(self._user_certs.get(user_id, set()))
        trust_score = self._user_trust_scores.get(user_id, 0.5)
        simulations = self._user_simulations.get(user_id, 0)
        xr_exams = self._user_xr_exams.get(user_id, 0)
        
        eligible, tier, unmet = self.evaluator.evaluate(
            user_certs=certs,
            user_trust_score=trust_score,
            user_simulations_passed=simulations,
            user_xr_exams_passed=xr_exams,
            task_family=task_family,
        )
        
        return {
            "user_id": user_id,
            "task_family": task_family,
            "eligible": eligible,
            "tier": tier.value if tier else None,
            "unmet_requirements": unmet,
            "current_stats": {
                "certs": len(certs),
                "trust_score": trust_score,
                "simulations": simulations,
                "xr_exams": xr_exams,
            },
        }
    
    def generate_proof(
        self,
        user_id: str,
        assessment_proofs: List[str] = None,
    ) -> EligibilityProof:
        """Generate eligibility proof for user"""
        certs = list(self._user_certs.get(user_id, set()))
        trust_score = self._user_trust_scores.get(user_id, 0.5)
        
        proof = self.proof_gen.generate(
            user_id=user_id,
            certs=certs,
            trust_score=trust_score,
            assessment_proofs=assessment_proofs or [],
        )
        
        self._proofs[proof.proof_id] = proof
        return proof
    
    def create_task_offer(
        self,
        user_id: str,
        task_id: str,
        task_family: str,
        task_complexity: float,
        task_risk: SkillCategory = SkillCategory.CATEGORY_A,
        skill_scarcity: float = 0.3,
    ) -> Optional[TaskEquityOffer]:
        """
        Create task offer for eligible user.
        
        Per spec: L'utilisateur CHOISIT une mission
        """
        # Check eligibility
        eligibility = self.check_eligibility(user_id, task_family)
        
        if not eligibility["eligible"]:
            logger.warning(f"User {user_id} not eligible for {task_family}")
            return None
        
        tier = EligibilityTier(eligibility["tier"])
        trust_score = self._user_trust_scores.get(user_id, 0.5)
        
        offer = self.offer_gen.generate_offer(
            task_id=task_id,
            user_id=user_id,
            tier=tier,
            task_complexity=task_complexity,
            task_risk=task_risk,
            skill_scarcity=skill_scarcity,
            trust_score=trust_score,
        )
        
        logger.info(
            f"Created offer {offer.offer_id} for user {user_id}: "
            f"salary={offer.salary_split:.2f}, equity={offer.equity_split:.1%}"
        )
        
        return offer
    
    def get_unlocked_opportunities(
        self,
        user_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Get all task families user is now eligible for.
        
        Per spec: UI affiche "Nouvelles opportunités débloquées"
        """
        opportunities = []
        
        for family in self.evaluator._rules_by_family.keys():
            eligibility = self.check_eligibility(user_id, family)
            if eligibility["eligible"]:
                opportunities.append({
                    "task_family": family,
                    "tier": eligibility["tier"],
                    "equity_rate": TIER_EQUITY_RATES.get(
                        EligibilityTier(eligibility["tier"]),
                        0
                    ),
                })
        
        return opportunities
    
    def get_progression_summary(
        self,
        user_id: str,
    ) -> Dict[str, Any]:
        """
        Get user progression summary.
        
        Per spec: tableau "progression → equity unlocked"
        """
        certs = list(self._user_certs.get(user_id, set()))
        trust_score = self._user_trust_scores.get(user_id, 0.5)
        simulations = self._user_simulations.get(user_id, 0)
        xr_exams = self._user_xr_exams.get(user_id, 0)
        
        unlocked = self.get_unlocked_opportunities(user_id)
        
        total_potential_equity = sum(
            opp.get("equity_rate", 0) for opp in unlocked
        )
        
        return {
            "user_id": user_id,
            "certifications": len(certs),
            "trust_score": trust_score,
            "simulations_passed": simulations,
            "xr_exams_passed": xr_exams,
            "unlocked_opportunities": len(unlocked),
            "total_potential_equity": total_potential_equity,
            "opportunities": unlocked,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_bridge() -> SkillToEquityBridge:
    """Create skill to equity bridge"""
    return SkillToEquityBridge()


def create_eligibility_rule(
    task_family: str,
    required_certs: List[str],
    min_trust_score: float = 0.7,
    tier: EligibilityTier = EligibilityTier.TIER_1,
) -> EligibilityRule:
    """Create eligibility rule"""
    return EligibilityRule(
        rule_id=generate_id(),
        task_family=task_family,
        required_certs=required_certs,
        min_trust_score=min_trust_score,
        tier=tier,
    )
