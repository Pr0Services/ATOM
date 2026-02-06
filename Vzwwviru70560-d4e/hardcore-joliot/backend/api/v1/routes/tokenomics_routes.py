"""
AT·OM Tokenomics API Routes
============================

API endpoints for the AT·OM economic system.

Author: AT·OM Collective
"""

from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Optional, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger("nova999.tokenomics_routes")

router = APIRouter(tags=["Tokenomics"])


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class ContributeRequest(BaseModel):
    """Process an investment contribution."""
    contributor_id: Optional[str] = Field(None, description="Contributor UUID (auto-generated if empty)")
    amount_usd: float = Field(..., gt=0, description="Contribution amount in USD")
    flow_type: Optional[str] = Field(None, description="Flow direction: tech, vie, sagesse, justice, graine, terre")
    message: Optional[str] = Field(None, max_length=500, description="Personal message to engrave")


class ConvertJTRequest(BaseModel):
    """Convert JT to UR."""
    contributor_id: str = Field(..., description="Contributor UUID")
    jt_amount: float = Field(..., gt=0, description="Amount of JT to convert")
    contribution_date: Optional[str] = Field(None, description="ISO date of original contribution")


class ATOMTradeRequest(BaseModel):
    """Buy or sell ATOM tokens."""
    amount_tokens: float = Field(..., gt=0, description="Number of ATOM tokens")


class ATOMQuoteRequest(BaseModel):
    """Get a quote for ATOM buy/sell."""
    action: str = Field(..., pattern="^(buy|sell)$", description="'buy' or 'sell'")
    amount_tokens: float = Field(..., gt=0, description="Number of ATOM tokens")


class FlowRequest(BaseModel):
    """Flow Keeper contribution."""
    contributor_id: Optional[str] = Field(None, description="Contributor UUID")
    amount_usd: float = Field(..., gt=0, description="Flow amount in USD")
    flow_type: str = Field(..., description="Flow type: tech, vie, sagesse, justice, graine, terre")
    message: Optional[str] = Field(None, max_length=500, description="Personal message")


class URMintRequest(BaseModel):
    """Mint UR tokens (admin only)."""
    amount: float = Field(..., gt=0, description="Amount of UR to mint")
    reason: str = Field(..., min_length=3, description="Reason for minting")


class URBurnRequest(BaseModel):
    """Burn UR tokens (admin only)."""
    amount: float = Field(..., gt=0, description="Amount of UR to burn")
    reason: str = Field(..., min_length=3, description="Reason for burning")


# =============================================================================
# CONTRIBUTION ENDPOINTS
# =============================================================================

@router.post(
    "/contribute",
    summary="Process contribution",
    description="Process a contribution to the AT·OM ecosystem.",
)
async def contribute(request: ContributeRequest):
    """Main contribution endpoint — JT + NFT + Flow Token in one transaction."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service, FlowType
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service, FlowType

        service = get_tokenomics_service()
        contributor_id = request.contributor_id or str(uuid4())

        flow_type = None
        if request.flow_type:
            try:
                flow_type = FlowType(request.flow_type.lower())
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid flow type: {request.flow_type}. Valid: tech, vie, sagesse, justice, graine, terre"
                )

        result = service.process_contribution(
            contributor_id=contributor_id,
            amount_usd=Decimal(str(request.amount_usd)),
            flow_type=flow_type,
            message=request.message,
        )

        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)

        return {
            "success": True,
            "data": result.to_dict(),
            "meta": {"engine": "TokenomicsService", "version": "1.0"},
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contribution error: {str(e)}")


@router.post(
    "/convert-jt",
    summary="Convert JT to UR",
    description="Convert JT to UR.",
)
async def convert_jt(request: ConvertJTRequest):
    """Convert JT to UR with seniority-based bonus rates."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        result = service.convert_jt_to_ur(
            contributor_id=request.contributor_id,
            jt_amount=Decimal(str(request.jt_amount)),
            contribution_date=request.contribution_date,
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")


# =============================================================================
# ECONOMY DASHBOARD ENDPOINTS
# =============================================================================

@router.get(
    "/economy",
    summary="Full economy state",
    description="Get current economy state.",
)
async def get_economy():
    """Full economy dashboard."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        return {
            "success": True,
            "data": service.get_economy_state(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/momentum",
    summary="Momentum progress",
    description="Get momentum progress.",
)
async def get_momentum():
    """Momentum progress for the landing page."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        state = service.get_economy_state()
        return {
            "success": True,
            "data": state["momentum_progress"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/nft-availability",
    summary="NFT availability per tier",
    description="Get NFT availability.",
)
async def get_nft_availability():
    """NFT availability for the inscription pages."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        state = service.get_economy_state()
        return {
            "success": True,
            "data": state["nft_availability"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/contributions",
    summary="Recent contributions",
    description="Get recent contributions.",
)
async def get_contributions(limit: int = 20):
    """Recent contribution history."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        return {
            "success": True,
            "data": service.get_contribution_history(limit=min(limit, 100)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ATOM BONDING CURVE ENDPOINTS
# =============================================================================

@router.post(
    "/atom/buy",
    summary="Buy ATOM tokens",
    description="Buy ATOM tokens.",
)
async def buy_atom(request: ATOMTradeRequest):
    """Buy ATOM tokens."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        result = service.buy_atom(Decimal(str(request.amount_tokens)))

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result["quote"]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/atom/sell",
    summary="Sell ATOM tokens",
    description="Sell ATOM tokens.",
)
async def sell_atom(request: ATOMTradeRequest):
    """Sell ATOM tokens."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        result = service.sell_atom(Decimal(str(request.amount_tokens)))

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result["quote"]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/atom/quote",
    summary="Get ATOM price quote",
    description="Get a price quote.",
)
async def atom_quote(action: str = "buy", amount: float = 100):
    """Get a price quote for ATOM buy/sell."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        if action not in ("buy", "sell"):
            raise HTTPException(status_code=400, detail="Action must be 'buy' or 'sell'")

        service = get_tokenomics_service()
        result = service.get_atom_quote(action, Decimal(str(amount)))

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result["quote"]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/atom/chart",
    summary="Bonding curve chart data",
    description="Get chart data.",
)
async def atom_chart(points: int = 50):
    """Bonding curve chart data for visualization."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        return {
            "success": True,
            "data": service.get_price_chart_data(points=min(points, 200)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/atom/state",
    summary="Current ATOM state",
    description="Get current ATOM state.",
)
async def atom_state():
    """Current ATOM bonding curve state."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        return {
            "success": True,
            "data": service.bonding_curve.get_state(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# FLOW KEEPER ENDPOINTS
# =============================================================================

@router.post(
    "/flow",
    summary="Flow Keeper contribution",
    description="Process a Flow Keeper contribution.",
)
async def contribute_flow(request: FlowRequest):
    """Flow Keeper — voluntary community stimulus."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service, FlowType
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service, FlowType

        service = get_tokenomics_service()
        contributor_id = request.contributor_id or str(uuid4())

        try:
            flow_type = FlowType(request.flow_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid flow type: {request.flow_type}. Valid: tech, vie, sagesse, justice, graine, terre"
            )

        result = service.process_flow(
            contributor_id=contributor_id,
            amount_usd=Decimal(str(request.amount_usd)),
            flow_type=flow_type,
            message=request.message,
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/flow/wall",
    summary="Flow Wall (live feed)",
    description="Get recent Flow Keeper contributions.",
)
async def flow_wall(limit: int = 50):
    """Flow Wall — recent contributions for live display."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        return {
            "success": True,
            "data": service.get_flow_history(limit=min(limit, 200)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/flow/stats",
    summary="Flow stats by type",
    description="Get Flow statistics.",
)
async def flow_stats():
    """Flow Keeper stats by type."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        state = service.get_economy_state()
        return {
            "success": True,
            "data": {
                "total": state["flow_total"],
                "by_type": state["flow_by_type"],
                "token_count": state["flow_token_count"],
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# UR ADMINISTRATION ENDPOINTS
# =============================================================================

@router.post(
    "/ur/mint",
    summary="Mint UR tokens (admin)",
    description="Admin operation.",
)
async def mint_ur(request: URMintRequest):
    """Admin: Mint UR tokens."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        result = service.mint_ur(
            amount=Decimal(str(request.amount)),
            reason=request.reason,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/ur/burn",
    summary="Burn UR tokens (admin)",
    description="Admin operation.",
)
async def burn_ur(request: URBurnRequest):
    """Admin: Burn UR tokens."""
    try:
        try:
            from services.tokenomics_service import get_tokenomics_service
        except ImportError:
            from backend.services.tokenomics_service import get_tokenomics_service

        service = get_tokenomics_service()
        result = service.burn_ur(
            amount=Decimal(str(request.amount)),
            reason=request.reason,
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {"success": True, "data": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
