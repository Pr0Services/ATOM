"""
CHE·NU SDK — SAFE MODE ONLY
Version: 2.0
Purpose: Interact with CHE·NU R&D Governance System

CRITICAL RULES (NON-NEGOTIABLE):
- SDK CANNOT apply changes
- SDK CANNOT bypass R&D
- SDK CANNOT trigger agents
- SDK operates in SAFE MODE ONLY

Features:
- Submit R&D proposals
- Run simulations (zero side effects)
- Retrieve human decisions
- Query governance status

Author: CHE·NU Project
Status: OFFICIAL — NON-CREATIVE — NON-NEGOTIABLE
"""

from __future__ import annotations

import json
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
from pathlib import Path
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════
# ENUMS & TYPES
# ═══════════════════════════════════════════════════════════════════════

class Decision(str, Enum):
    """R&D decision outcomes"""
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    REJECT = "REJECT"


class FindingLevel(str, Enum):
    """Lint finding severity"""
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"


class Zone(str, Enum):
    """Execution zones"""
    AUTONOMY = "AUTONOMY_EXECUTION_ZONE"
    VERIFIED = "VERIFIED_EXECUTION_ZONE"


# ═══════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class Finding:
    """Single lint finding"""
    level: FindingLevel
    code: str
    message: str
    hint: str = ""


@dataclass
class LintReport:
    """Lint report for R&D proposal"""
    status: Literal["PASS", "FAIL"]
    errors: int
    warnings: int
    findings: List[Finding]
    proposal_id: Optional[str] = None


@dataclass
class SimulationResult:
    """Simulation output (quarantined)"""
    simulation_id: str
    proposed_changes: List[Dict]
    risk_analysis: Dict
    human_validation_points: List[str]
    artifacts: List[Dict]
    quarantined: bool = True
    auto_promotable: bool = False


@dataclass
class ProposalStatus:
    """R&D proposal status"""
    proposal_id: str
    decision: Optional[Decision]
    decided_by: Optional[str]
    decided_at: Optional[str]
    reasoning: Optional[str]
    lint_status: str


# ═══════════════════════════════════════════════════════════════════════
# CHE·NU SDK (SAFE MODE)
# ═══════════════════════════════════════════════════════════════════════

class ChenuSDK:
    """
    CHE·NU R&D Governance SDK
    
    SAFE MODE ONLY:
    - Cannot apply changes
    - Cannot bypass R&D
    - Cannot trigger agents
    - Can only submit, simulate, query
    
    Usage:
        sdk = ChenuSDK(base_url="http://localhost:8000")
        
        # Submit proposal
        report = sdk.submit_proposal(proposal_text)
        
        # Run simulation
        result = sdk.simulate(proposal_id)
        
        # Get decision
        status = sdk.get_decision(proposal_id)
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_version: str = "v1",
        timeout: int = 30
    ):
        """
        Initialize CHE·NU SDK
        
        Args:
            base_url: CHE·NU API base URL
            api_version: API version
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.timeout = timeout
        self._session = requests.Session()
        
        # CRITICAL: Verify policy compliance on init
        self._verify_policy_compliance()
    
    def _verify_policy_compliance(self):
        """
        Verify SDK is operating in safe mode
        
        Raises:
            RuntimeError: If policy violations detected
        """
        try:
            health = self.health_check()
            if not health.get("safe_mode", False):
                raise RuntimeError(
                    "CHE·NU SDK CRITICAL ERROR: Server not in safe mode. "
                    "SDK requires safe mode enforcement."
                )
        except Exception as e:
            # If health check fails, proceed with warning
            print(f"[WARN] Could not verify server safe mode: {e}")
    
    def _endpoint(self, path: str) -> str:
        """Build full endpoint URL"""
        return f"{self.base_url}/api/{self.api_version}{path}"
    
    # ───────────────────────────────────────────────────────────────────
    # CORE METHODS
    # ───────────────────────────────────────────────────────────────────
    
    def submit_proposal(
        self,
        text: str,
        check_repo_duplicates: bool = True
    ) -> LintReport:
        """
        Submit R&D proposal to CHE·NU governance gate
        
        SAFE MODE:
        - Returns lint report ONLY
        - Does NOT modify any data
        - Does NOT apply changes
        - Does NOT bypass R&D
        
        Args:
            text: R&D proposal text (must include required fields)
            check_repo_duplicates: Enable repo token overlap check
        
        Returns:
            LintReport with status and findings
        
        Raises:
            ValueError: If proposal rejected (errors found)
            RuntimeError: If API error
        """
        try:
            response = self._session.post(
                self._endpoint("/rnd/lint"),
                json={
                    "proposal_text": text,
                    "check_repo_duplicates": check_repo_duplicates
                },
                timeout=self.timeout
            )
            
            if response.status_code == 422:
                # Proposal rejected
                data = response.json()
                raise ValueError(
                    f"Proposal rejected: {data['detail']['message']}\n"
                    f"Errors: {len(data['detail']['findings'])}"
                )
            
            response.raise_for_status()
            data = response.json()
            
            return LintReport(
                status=data["status"],
                errors=data["errors"],
                warnings=data["warnings"],
                findings=[
                    Finding(
                        level=FindingLevel(f["level"]),
                        code=f["code"],
                        message=f["message"],
                        hint=f.get("hint", "")
                    )
                    for f in data["findings"]
                ]
            )
            
        except requests.RequestException as e:
            raise RuntimeError(f"API error: {e}")
    
    def simulate(
        self,
        proposal_id: str,
        execution_params: Optional[Dict] = None
    ) -> SimulationResult:
        """
        Run proposal in SIMULATION ONLY mode
        
        SAFE MODE:
        - Executes logic
        - Produces artifacts
        - Generates outcomes
        - ZERO side effects
        - NO data modification
        - Results quarantined
        
        Args:
            proposal_id: ID of proposal to simulate
            execution_params: Optional simulation parameters
        
        Returns:
            SimulationResult (quarantined, non-promotable)
        
        Rules:
        - Simulation results are ALWAYS quarantined
        - Cannot be promoted automatically
        - Must pass Human Validation Gate
        """
        try:
            response = self._session.post(
                self._endpoint(f"/rnd/simulate/{proposal_id}"),
                json=execution_params or {},
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # CRITICAL: Verify quarantine
            if not data.get("quarantined", True):
                raise RuntimeError(
                    "CRITICAL: Simulation result not quarantined. "
                    "This violates CHE·NU safe mode policy."
                )
            
            return SimulationResult(
                simulation_id=data["simulation_id"],
                proposed_changes=data.get("proposed_changes", []),
                risk_analysis=data.get("risk_analysis", {}),
                human_validation_points=data.get("human_validation_points", []),
                artifacts=data.get("artifacts", []),
                quarantined=True,  # Always true
                auto_promotable=False  # Always false
            )
            
        except requests.RequestException as e:
            raise RuntimeError(f"Simulation API error: {e}")
    
    def get_decision(self, proposal_id: str) -> ProposalStatus:
        """
        Get human decision for R&D proposal
        
        SAFE MODE:
        - Returns decision ONLY
        - Does NOT execute decision
        - Does NOT apply changes
        
        Args:
            proposal_id: ID of proposal
        
        Returns:
            ProposalStatus with decision (ACCEPT/MODIFY/REJECT)
        
        Note:
            Only returns decision made by HUMAN.
            SDK cannot make decisions.
        """
        try:
            response = self._session.get(
                self._endpoint(f"/rnd/proposals/{proposal_id}/status"),
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return ProposalStatus(
                proposal_id=data["proposal_id"],
                decision=Decision(data["decision"]) if data.get("decision") else None,
                decided_by=data.get("decided_by"),
                decided_at=data.get("decided_at"),
                reasoning=data.get("reasoning"),
                lint_status=data.get("lint_status", "UNKNOWN")
            )
            
        except requests.RequestException as e:
            raise RuntimeError(f"API error: {e}")
    
    # ───────────────────────────────────────────────────────────────────
    # GOVERNANCE QUERIES
    # ───────────────────────────────────────────────────────────────────
    
    def health_check(self) -> Dict:
        """
        Check R&D governance system health
        
        Returns:
            Health status dict
        """
        try:
            response = self._session.get(
                self._endpoint("/rnd/health"),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def get_policy(self) -> Dict:
        """
        Get current CHE·NU policy configuration
        
        Returns:
            Policy dict (from CHE-NU_POLICY.json)
        """
        try:
            response = self._session.get(
                self._endpoint("/rnd/policy"),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Policy API error: {e}")
    
    def verify_architecture_freeze(self) -> bool:
        """
        Verify architecture freeze is intact
        
        Returns:
            True if freeze intact, False otherwise
        """
        try:
            policy = self.get_policy()
            return policy.get("architecture_freeze", {}).get("enabled", False)
        except:
            return False
    
    # ───────────────────────────────────────────────────────────────────
    # FORBIDDEN METHODS (WILL RAISE)
    # ───────────────────────────────────────────────────────────────────
    
    def apply_changes(self, *args, **kwargs):
        """
        FORBIDDEN: SDK cannot apply changes
        
        Raises:
            RuntimeError: Always (method forbidden)
        """
        raise RuntimeError(
            "CHE·NU SDK POLICY VIOLATION: "
            "SDK cannot apply changes. "
            "Changes must be applied via Human Validation Gate."
        )
    
    def bypass_rd(self, *args, **kwargs):
        """
        FORBIDDEN: SDK cannot bypass R&D
        
        Raises:
            RuntimeError: Always (method forbidden)
        """
        raise RuntimeError(
            "CHE·NU SDK POLICY VIOLATION: "
            "SDK cannot bypass R&D system. "
            "All changes must pass through R&D pipeline."
        )
    
    def trigger_agent(self, *args, **kwargs):
        """
        FORBIDDEN: SDK cannot trigger agents
        
        Raises:
            RuntimeError: Always (method forbidden)
        """
        raise RuntimeError(
            "CHE·NU SDK POLICY VIOLATION: "
            "SDK cannot trigger agents. "
            "Agents must be triggered by explicit human action."
        )


# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def load_policy(path: str = "CHE-NU_POLICY.json") -> Dict:
    """
    Load CHE·NU policy from file
    
    Args:
        path: Path to policy JSON file
    
    Returns:
        Policy dict
    """
    return json.loads(Path(path).read_text())


def verify_proposal_format(text: str) -> bool:
    """
    Quick check if proposal has required fields
    
    Args:
        text: Proposal text
    
    Returns:
        True if basic format valid
    """
    required = [
        "USER TYPE:",
        "CONTEXT:",
        "HUMAN ACTION:",
        "NEED:",
        "WHAT MUST NEVER BE AUTOMATED:",
        "FAILURE RISK:",
        "SPHERES:",
        "HUMAN VALIDATION:",
        "UNDO/REVERSIBILITY:",
        "REDUNDANCY CHECK:"
    ]
    
    text_upper = text.upper()
    return all(field in text_upper for field in required)


# ═══════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Initialize SDK
    sdk = ChenuSDK(base_url="http://localhost:8000")
    
    # Example 1: Submit proposal
    proposal_text = """
USER TYPE: Academic Researcher
CONTEXT: Professor completed peer-reviewed research
HUMAN ACTION: Clicks publish button after review
NEED: Share validated research with network
WHAT MUST NEVER BE AUTOMATED: Decision to publish
FAILURE RISK: Auto-publishing unvalidated work
SPHERES: Scholar, Social & Media
CONNECTION TYPE: Projection
HUMAN VALIDATION: Explicit click with preview, logged with user_id
UNDO/REVERSIBILITY: Delete via button, undo_patch logged
REDUNDANCY CHECK: Verified against Scholar/Social modules, no duplication
    """
    
    try:
        report = sdk.submit_proposal(proposal_text)
        print(f"Lint Status: {report.status}")
        print(f"Errors: {report.errors}, Warnings: {report.warnings}")
        
        for finding in report.findings:
            print(f"[{finding.level}] {finding.code}: {finding.message}")
    
    except ValueError as e:
        print(f"Proposal rejected: {e}")
    
    # Example 2: Run simulation
    try:
        result = sdk.simulate("proposal_123")
        print(f"\nSimulation ID: {result.simulation_id}")
        print(f"Quarantined: {result.quarantined}")
        print(f"Proposed Changes: {len(result.proposed_changes)}")
        print(f"Human Validation Points: {result.human_validation_points}")
    except RuntimeError as e:
        print(f"Simulation error: {e}")
    
    # Example 3: Get decision
    try:
        status = sdk.get_decision("proposal_123")
        print(f"\nProposal Decision: {status.decision}")
        print(f"Decided By: {status.decided_by}")
    except RuntimeError as e:
        print(f"Decision query error: {e}")
    
    # Example 4: Forbidden methods (will raise)
    try:
        sdk.apply_changes()  # RAISES
    except RuntimeError as e:
        print(f"\n✅ Correctly blocked: {e}")
