"""
CHE·NU R&D GOVERNANCE — FASTAPI INTEGRATION
Version: 1.0

Provides:
  1) API endpoint to lint proposals
  2) Guard middleware to block non-compliant feature deployments
  3) Auto-rejection of proposals with errors

Usage:
  from chenu_rnd_api import install_rnd_governance
  
  app = FastAPI()
  install_rnd_governance(app, repo_path="/path/to/project")
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import subprocess
import tempfile
from pathlib import Path

# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class ProposalLintRequest(BaseModel):
    """Request to lint R&D proposal"""
    proposal_text: str
    check_repo_duplicates: bool = True

class FindingResponse(BaseModel):
    """Single lint finding"""
    level: str
    code: str
    message: str
    hint: str = ""

class LintResponse(BaseModel):
    """Lint result"""
    status: str  # "PASS" | "FAIL"
    errors: int
    warnings: int
    findings: List[FindingResponse]

# ─────────────────────────────────────────────
# R&D LINTER INTEGRATION
# ─────────────────────────────────────────────

def lint_proposal(text: str, repo_path: str | None = None) -> LintResponse:
    """
    Lint R&D proposal using chenu_rnd_lint_allinone.py
    
    Returns:
        LintResponse with status and findings
    """
    # Write proposal to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(text)
        temp_path = f.name
    
    try:
        # Build command
        cmd = [
            "python3",
            "tools/chenu_rnd_lint_allinone.py",
            "--in", temp_path,
            "--json", f"{temp_path}.json"
        ]
        
        if repo_path:
            cmd.extend(["--repo", repo_path])
        
        # Run linter
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse JSON output
        import json
        report_path = Path(f"{temp_path}.json")
        if report_path.exists():
            data = json.loads(report_path.read_text())
            
            # Extract findings from first proposal
            findings = []
            if data.get("reports"):
                for f in data["reports"][0].get("findings", []):
                    findings.append(FindingResponse(
                        level=f["level"],
                        code=f["code"],
                        message=f["message"],
                        hint=f.get("hint", "")
                    ))
            
            errors = data["summary"]["errors"]
            warnings = data["summary"]["warnings"]
            
            return LintResponse(
                status="PASS" if errors == 0 else "FAIL",
                errors=errors,
                warnings=warnings,
                findings=findings
            )
        else:
            raise Exception("Linter did not produce JSON output")
            
    finally:
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
        Path(f"{temp_path}.json").unlink(missing_ok=True)

# ─────────────────────────────────────────────
# FASTAPI ROUTES
# ─────────────────────────────────────────────

def create_rnd_router(repo_path: str | None = None):
    """Create FastAPI router for R&D governance"""
    from fastapi import APIRouter
    
    router = APIRouter(prefix="/api/v1/rnd", tags=["R&D Governance"])
    
    @router.post("/lint", response_model=LintResponse)
    async def lint_rnd_proposal(request: ProposalLintRequest):
        """
        Lint R&D proposal against CHE·NU canonical rules.
        
        Returns PASS/FAIL with detailed findings.
        Proposals with ERRORs are automatically rejected.
        """
        try:
            result = lint_proposal(
                request.proposal_text,
                repo_path if request.check_repo_duplicates else None
            )
            
            if result.status == "FAIL":
                # Auto-reject proposals with errors
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "RND_PROPOSAL_REJECTED",
                        "message": f"Proposal failed R&D lint with {result.errors} error(s)",
                        "findings": [f.dict() for f in result.findings if f.level == "ERROR"]
                    }
                )
            
            return result
            
        except subprocess.TimeoutExpired:
            raise HTTPException(
                status_code=500,
                detail="R&D linter timeout"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"R&D lint error: {str(e)}"
            )
    
    @router.get("/health")
    async def rnd_health():
        """Check R&D governance system health"""
        linter_exists = Path("tools/chenu_rnd_lint_allinone.py").exists()
        return {
            "status": "healthy" if linter_exists else "degraded",
            "linter_available": linter_exists,
            "frozen_spheres": 9,
            "connection_types": 4
        }
    
    return router

# ─────────────────────────────────────────────
# GUARD MIDDLEWARE (BLOCKS NON-COMPLIANT FEATURES)
# ─────────────────────────────────────────────

class RnDGuardMiddleware:
    """
    Middleware that blocks deployment of features without R&D approval.
    
    Checks for x-chenu-rnd-approved header on feature-related endpoints.
    If header missing or invalid, blocks request.
    """
    
    def __init__(self, app, protected_prefixes: List[str] = None):
        self.app = app
        self.protected_prefixes = protected_prefixes or [
            "/api/v1/features",
            "/api/v1/modules",
            "/api/v1/connections"
        ]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            method = scope["method"]
            
            # Check if this is a protected endpoint
            if method in ["POST", "PUT", "PATCH"] and any(
                path.startswith(prefix) for prefix in self.protected_prefixes
            ):
                # Check for R&D approval header
                headers = dict(scope.get("headers", []))
                rnd_approved = headers.get(b"x-chenu-rnd-approved", b"").decode()
                
                if not rnd_approved or rnd_approved != "true":
                    # Block request
                    response = JSONResponse(
                        status_code=403,
                        content={
                            "error": "RND_APPROVAL_REQUIRED",
                            "message": "Feature deployment requires R&D approval",
                            "hint": "Submit proposal via /api/v1/rnd/lint first"
                        }
                    )
                    await response(scope, receive, send)
                    return
        
        await self.app(scope, receive, send)

# ─────────────────────────────────────────────
# INSTALLATION
# ─────────────────────────────────────────────

def install_rnd_governance(
    app: FastAPI,
    repo_path: str | None = None,
    enable_guard: bool = True,
    protected_prefixes: List[str] = None
):
    """
    Install R&D governance system on FastAPI app.
    
    Args:
        app: FastAPI application
        repo_path: Path to existing repo for duplication check
        enable_guard: Enable guard middleware (blocks non-approved features)
        protected_prefixes: API prefixes requiring R&D approval
    
    Example:
        app = FastAPI()
        install_rnd_governance(
            app,
            repo_path="/path/to/project",
            enable_guard=True
        )
    """
    # Install routes
    router = create_rnd_router(repo_path)
    app.include_router(router)
    
    # Install guard middleware
    if enable_guard:
        app.add_middleware(
            RnDGuardMiddleware,
            protected_prefixes=protected_prefixes
        )
    
    print("[CHE·NU] R&D Governance installed")
    print(f"  - Linter endpoint: /api/v1/rnd/lint")
    print(f"  - Health check: /api/v1/rnd/health")
    if enable_guard:
        print(f"  - Guard middleware: ACTIVE")

# ─────────────────────────────────────────────
# EXAMPLE USAGE
# ─────────────────────────────────────────────

"""
# main.py

from fastapi import FastAPI
from chenu_rnd_api import install_rnd_governance

app = FastAPI(title="CHE·NU API")

# Install canonical safety (from previous block)
from chenu_canonical_middleware import install_chenu_safety
install_chenu_safety(app)

# Install R&D governance
install_rnd_governance(
    app,
    repo_path="/path/to/chenu/project",
    enable_guard=True
)

# Your other routes...
from api.myteam import router as myteam_router
app.include_router(myteam_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
