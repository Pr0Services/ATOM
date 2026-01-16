"""
============================================================================
CHE·NU™ V69 — LAB-SPACE XR WORKBENCH
============================================================================
Spec: GPT1/CHE-NU_LAB_WORKBENCH_XR.md

Description: Interface XR où l'utilisateur manipule des Artifacts.

Tools:
- Stress-Testeur
- Réacteur de Synthèse
- Chronos (accélérateur temporel)
- Spectromètre causal

Governance: Read-only, signatures immuables, export certifié.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import copy

from ..models import (
    WorkbenchArtifact,
    WorkbenchTool,
    ToolResult,
    XRPack,
    generate_id,
    compute_hash,
    sign_xr_pack,
)

logger = logging.getLogger(__name__)


# ============================================================================
# WORKBENCH TOOLS
# ============================================================================

class StressTester:
    """
    Stress testing tool.
    
    Per spec: Stress-Testeur
    """
    
    def test(
        self,
        artifact: WorkbenchArtifact,
        stress_factor: float = 2.0,
    ) -> ToolResult:
        """Apply stress test to artifact"""
        stressed_data = copy.deepcopy(artifact.data)
        
        # Apply stress to numeric values
        for key, value in stressed_data.items():
            if isinstance(value, (int, float)):
                stressed_data[key] = value * stress_factor
        
        result = ToolResult(
            tool=WorkbenchTool.STRESS_TESTER,
            input_artifact=artifact.artifact_id,
            output_data={
                "original": artifact.data,
                "stressed": stressed_data,
                "factor": stress_factor,
                "stability": self._compute_stability(artifact.data, stressed_data),
            },
        )
        
        logger.info(f"Stress test on {artifact.name}: factor={stress_factor}")
        return result
    
    def _compute_stability(
        self,
        original: Dict[str, Any],
        stressed: Dict[str, Any],
    ) -> float:
        """Compute stability score"""
        total_delta = 0.0
        count = 0
        
        for key in original:
            if isinstance(original[key], (int, float)):
                orig_val = original[key]
                stress_val = stressed.get(key, 0)
                if orig_val != 0:
                    total_delta += abs(stress_val - orig_val) / abs(orig_val)
                    count += 1
        
        return 1.0 - min(1.0, total_delta / count) if count > 0 else 1.0


class SynthesisReactor:
    """
    Synthesis reactor tool.
    
    Per spec: Réacteur de Synthèse
    """
    
    def synthesize(
        self,
        artifacts: List[WorkbenchArtifact],
    ) -> ToolResult:
        """Synthesize multiple artifacts into one"""
        combined_data = {}
        
        for artifact in artifacts:
            for key, value in artifact.data.items():
                if key in combined_data:
                    # Combine numeric values
                    if isinstance(value, (int, float)):
                        combined_data[key] = (combined_data[key] + value) / 2
                    else:
                        combined_data[f"{key}_merged"] = value
                else:
                    combined_data[key] = value
        
        result = ToolResult(
            tool=WorkbenchTool.SYNTHESIS_REACTOR,
            input_artifact=",".join(a.artifact_id for a in artifacts),
            output_data={
                "synthesized": combined_data,
                "source_count": len(artifacts),
            },
        )
        
        logger.info(f"Synthesized {len(artifacts)} artifacts")
        return result


class Chronos:
    """
    Time accelerator tool.
    
    Per spec: Chronos (accélérateur temporel)
    """
    
    def project(
        self,
        artifact: WorkbenchArtifact,
        months: int = 12,
        growth_rate: float = 0.05,
    ) -> ToolResult:
        """Project artifact data into the future"""
        projections = []
        current = copy.deepcopy(artifact.data)
        
        for m in range(months):
            projected = {}
            for key, value in current.items():
                if isinstance(value, (int, float)):
                    projected[key] = value * (1 + growth_rate)
                else:
                    projected[key] = value
            
            projections.append({
                "month": m + 1,
                "data": projected,
            })
            current = projected
        
        result = ToolResult(
            tool=WorkbenchTool.CHRONOS,
            input_artifact=artifact.artifact_id,
            output_data={
                "projections": projections,
                "horizon_months": months,
                "growth_rate": growth_rate,
            },
        )
        
        logger.info(f"Chronos projection: {months} months at {growth_rate:.1%} growth")
        return result


class CausalSpectrometer:
    """
    Causal analysis tool.
    
    Per spec: Spectromètre causal
    """
    
    def analyze(
        self,
        artifact: WorkbenchArtifact,
    ) -> ToolResult:
        """Analyze causal structure of artifact"""
        # Mock causal analysis
        causal_links = []
        keys = list(artifact.data.keys())
        
        for i in range(len(keys) - 1):
            if isinstance(artifact.data[keys[i]], (int, float)):
                causal_links.append({
                    "source": keys[i],
                    "target": keys[i + 1],
                    "strength": 0.5 + (i * 0.1),
                })
        
        result = ToolResult(
            tool=WorkbenchTool.CAUSAL_SPECTROMETER,
            input_artifact=artifact.artifact_id,
            output_data={
                "causal_links": causal_links,
                "complexity_score": len(causal_links) * 0.2,
                "stability_rating": 0.8,
            },
        )
        
        logger.info(f"Causal analysis: {len(causal_links)} links found")
        return result


# ============================================================================
# LAB WORKBENCH
# ============================================================================

class LabWorkbench:
    """
    XR Lab Workbench.
    
    Per spec: Interface XR où l'utilisateur manipule des Artifacts
    """
    
    def __init__(self):
        # Tools
        self.stress_tester = StressTester()
        self.synthesis_reactor = SynthesisReactor()
        self.chronos = Chronos()
        self.spectrometer = CausalSpectrometer()
        
        # Artifacts
        self._artifacts: Dict[str, WorkbenchArtifact] = {}
        self._results: List[ToolResult] = []
        
        # Session
        self._session_id = generate_id()
    
    def add_artifact(
        self,
        name: str,
        data: Dict[str, Any],
        position: Tuple[float, float, float] = None,
    ) -> WorkbenchArtifact:
        """Add artifact to workbench"""
        artifact = WorkbenchArtifact(
            artifact_id=generate_id(),
            name=name,
            data=data,
            position=position or (0.0, 0.0, 0.0),
        )
        
        self._artifacts[artifact.artifact_id] = artifact
        logger.info(f"Added artifact {name} to workbench")
        return artifact
    
    def select_artifact(self, artifact_id: str) -> Optional[WorkbenchArtifact]:
        """Select an artifact"""
        artifact = self._artifacts.get(artifact_id)
        if artifact:
            # Deselect others
            for a in self._artifacts.values():
                a.is_selected = False
            artifact.is_selected = True
        return artifact
    
    def use_tool(
        self,
        tool: WorkbenchTool,
        artifact_ids: List[str],
        **kwargs,
    ) -> Optional[ToolResult]:
        """Use a workbench tool"""
        artifacts = [
            self._artifacts[aid]
            for aid in artifact_ids
            if aid in self._artifacts
        ]
        
        if not artifacts:
            return None
        
        result = None
        
        if tool == WorkbenchTool.STRESS_TESTER:
            result = self.stress_tester.test(artifacts[0], **kwargs)
        
        elif tool == WorkbenchTool.SYNTHESIS_REACTOR:
            result = self.synthesis_reactor.synthesize(artifacts)
        
        elif tool == WorkbenchTool.CHRONOS:
            result = self.chronos.project(artifacts[0], **kwargs)
        
        elif tool == WorkbenchTool.CAUSAL_SPECTROMETER:
            result = self.spectrometer.analyze(artifacts[0])
        
        if result:
            self._results.append(result)
        
        return result
    
    def export_certified(self) -> XRPack:
        """
        Export certified XR pack.
        
        Per spec: export certifié
        """
        pack = XRPack(
            pack_id=generate_id(),
            session_id=self._session_id,
            artifacts=list(self._artifacts.values()),
            read_only=True,  # Per spec: Read-only
        )
        
        # Sign pack
        pack.signature = sign_xr_pack(pack, "lab_workbench")
        
        logger.info(f"Exported certified pack: {pack.pack_id}")
        return pack
    
    def get_xr_manifest(self) -> Dict[str, Any]:
        """Get XR manifest for rendering"""
        return {
            "type": "lab_workbench",
            "session_id": self._session_id,
            "artifacts": [
                {
                    "id": a.artifact_id,
                    "name": a.name,
                    "position": a.position,
                    "selected": a.is_selected,
                    "locked": a.is_locked,
                }
                for a in self._artifacts.values()
            ],
            "tools_available": [t.value for t in WorkbenchTool],
            "result_count": len(self._results),
            "read_only": True,  # Per spec
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_workbench() -> LabWorkbench:
    """Create lab workbench"""
    return LabWorkbench()
