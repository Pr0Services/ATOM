"""
Hedera API Routes for AT·OM Sovereign Economy

Provides REST endpoints for all Hedera operations including:
- UR token operations (mint, burn, transfer, balance)
- Account management
- Conversion requests (UR <-> Fiat)
- Economic dashboard data

All routes require authentication via JWT token.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime
import logging

from app.services.hedera_service import (
    get_hedera_service,
    HederaService,
    TransactionResult,
    URTokenInfo
)
from app.services.auth_service import get_current_user, require_sovereignty_level

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/hedera", tags=["hedera"])


# ==================== REQUEST/RESPONSE MODELS ====================

class MintRequest(BaseModel):
    """Request to mint new UR tokens"""
    amount: Decimal = Field(..., gt=0, description="Amount of UR to mint")
    reason: str = Field(..., min_length=3, max_length=500)
    recipient_account: Optional[str] = Field(None, description="Direct transfer to account")

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > Decimal('1000000000'):
            raise ValueError('Amount exceeds maximum allowed')
        return v


class BurnRequest(BaseModel):
    """Request to burn UR tokens"""
    amount: Decimal = Field(..., gt=0)
    reason: str = Field(..., min_length=3, max_length=500)


class TransferRequest(BaseModel):
    """Request to transfer UR tokens"""
    to_account: str = Field(..., regex=r'^0\.0\.\d+$')
    amount: Decimal = Field(..., gt=0)
    memo: Optional[str] = Field(None, max_length=100)


class ConversionRequest(BaseModel):
    """Request to convert between UR and fiat"""
    direction: str = Field(..., regex='^(ur_to_fiat|fiat_to_ur)$')
    amount: Decimal = Field(..., gt=0)
    currency: str = Field('CAD', regex='^(CAD|USD)$')
    payout_method: Optional[str] = Field(
        None,
        regex='^(bank_transfer|interac|virtual_card)$'
    )


class CreateAccountRequest(BaseModel):
    """Request to create a new sovereign account"""
    initial_hbar: Decimal = Field(default=Decimal('1.0'), ge=0)
    memo: Optional[str] = Field(None, max_length=100)


class AssociateTokenRequest(BaseModel):
    """Request to associate UR token with account"""
    account_id: str = Field(..., regex=r'^0\.0\.\d+$')
    account_key: str = Field(..., min_length=10)


class TransactionResponse(BaseModel):
    """Standard response for Hedera transactions"""
    success: bool
    transaction_id: Optional[str]
    status: Optional[str]
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BalanceResponse(BaseModel):
    """Response for balance queries"""
    account_id: str
    ur_balance: Decimal
    ur_locked: Decimal = Decimal('0')
    ur_pending: Decimal = Decimal('0')
    total_available: Decimal
    last_updated: datetime


class TokenInfoResponse(BaseModel):
    """Response for token info queries"""
    token_id: str
    name: str
    symbol: str
    decimals: int
    total_supply: str
    circulating_supply: str
    treasury_balance: str
    is_paused: bool


class EconomicDashboardResponse(BaseModel):
    """Response for economic dashboard"""
    ur_stats: Dict[str, Any]
    liquidity: Dict[str, Any]
    conversion_rate: Dict[str, Decimal]
    recent_activity: List[Dict[str, Any]]
    health_indicators: Dict[str, Any]


# ==================== HELPER FUNCTIONS ====================

def get_service() -> HederaService:
    """Get initialized Hedera service"""
    service = get_hedera_service()
    if not service.is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Hedera service not initialized"
        )
    return service


# ==================== TOKEN OPERATION ROUTES ====================

@router.post("/token/mint", response_model=TransactionResponse)
async def mint_ur_tokens(
    request: MintRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(7))  # SOVEREIGN only
):
    """
    Mint new UR tokens.

    Requires SOVEREIGN (level 7) permission.
    """
    service = get_service()

    result = await service.mint_ur(
        amount=request.amount,
        reason=request.reason,
        recipient_account=request.recipient_account
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    # Log in background
    background_tasks.add_task(
        service.log_economic_event,
        event_type="MINT",
        amount=request.amount,
        to_account=request.recipient_account,
        metadata={"reason": request.reason, "minted_by": user.get('id')}
    )

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data=result.metadata
    )


@router.post("/token/burn", response_model=TransactionResponse)
async def burn_ur_tokens(
    request: BurnRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(6))  # GUARDIAN+
):
    """
    Burn UR tokens from treasury.

    Requires GUARDIAN (level 6) or higher.
    """
    service = get_service()

    result = await service.burn_ur(
        amount=request.amount,
        reason=request.reason
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    background_tasks.add_task(
        service.log_economic_event,
        event_type="BURN",
        amount=request.amount,
        metadata={"reason": request.reason, "burned_by": user.get('id')}
    )

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data=result.metadata
    )


@router.post("/token/transfer", response_model=TransactionResponse)
async def transfer_ur_tokens(
    request: TransferRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Transfer UR tokens to another account.

    The sender is determined from the authenticated user's Hedera account.
    """
    service = get_service()

    # Get user's Hedera account from profile
    user_hedera_account = user.get('hedera_account_id')
    if not user_hedera_account:
        raise HTTPException(
            status_code=400,
            detail="User does not have a Hedera account. Please create one first."
        )

    # Verify sufficient balance
    success, balance, error = await service.get_ur_balance(user_hedera_account)
    if not success:
        raise HTTPException(status_code=400, detail=error)

    if balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance: {balance} UR available, {request.amount} UR requested"
        )

    result = await service.transfer_ur(
        from_account=user_hedera_account,
        to_account=request.to_account,
        amount=request.amount,
        memo=request.memo
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    background_tasks.add_task(
        service.log_economic_event,
        event_type="TRANSFER",
        amount=request.amount,
        from_account=user_hedera_account,
        to_account=request.to_account,
        metadata={"memo": request.memo, "initiated_by": user.get('id')}
    )

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data=result.metadata
    )


@router.get("/token/balance/{account_id}", response_model=BalanceResponse)
async def get_ur_balance(
    account_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get UR token balance for an account.

    Users can only query their own balance unless they have elevated permissions.
    """
    service = get_service()

    # Check if user is querying their own balance or has permissions
    user_account = user.get('hedera_account_id')
    user_level = user.get('sovereignty_level', 1)

    if account_id != user_account and user_level < 5:
        raise HTTPException(
            status_code=403,
            detail="Cannot query other users' balances"
        )

    success, balance, error = await service.get_ur_balance(account_id)

    if not success:
        raise HTTPException(status_code=400, detail=error)

    return BalanceResponse(
        account_id=account_id,
        ur_balance=balance,
        ur_locked=Decimal('0'),  # Would come from database
        ur_pending=Decimal('0'),  # Would come from database
        total_available=balance,
        last_updated=datetime.utcnow()
    )


@router.get("/token/info", response_model=TokenInfoResponse)
async def get_token_info(
    user: dict = Depends(get_current_user)
):
    """
    Get information about the UR token.
    """
    service = get_service()
    info = await service.get_token_info()

    if not info:
        raise HTTPException(
            status_code=404,
            detail="UR token not configured or not found"
        )

    return TokenInfoResponse(
        token_id=info.token_id,
        name=info.name,
        symbol=info.symbol,
        decimals=info.decimals,
        total_supply=str(info.total_supply),
        circulating_supply=str(info.circulating_supply),
        treasury_balance=str(info.treasury_balance),
        is_paused=info.is_paused
    )


# ==================== ACCOUNT ROUTES ====================

@router.post("/account/create", response_model=TransactionResponse)
async def create_sovereign_account(
    request: CreateAccountRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Create a new Hedera account for a sovereign member.

    Returns account ID and keys. The private key should be stored securely
    by the user - it will not be stored by the system.
    """
    service = get_service()

    # Check if user already has an account
    if user.get('hedera_account_id'):
        raise HTTPException(
            status_code=400,
            detail="User already has a Hedera account"
        )

    result = await service.create_sovereign_account(
        initial_balance_hbar=request.initial_hbar,
        memo=request.memo or f"AT·OM Sovereign: {user.get('id')}"
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    # Note: In production, trigger database update to link account to user
    # This should be done via a separate secure process

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data={
            'account_id': result.metadata.get('account_id'),
            'public_key': result.metadata.get('public_key'),
            # Private key returned only once - user must save it
            'private_key': result.metadata.get('private_key'),
            'warning': 'SAVE YOUR PRIVATE KEY SECURELY. It will not be shown again.'
        }
    )


@router.post("/account/associate", response_model=TransactionResponse)
async def associate_ur_token(
    request: AssociateTokenRequest,
    user: dict = Depends(get_current_user)
):
    """
    Associate UR token with a Hedera account.

    This must be done before the account can receive UR tokens.
    """
    service = get_service()

    # Verify user owns this account
    user_account = user.get('hedera_account_id')
    if request.account_id != user_account:
        raise HTTPException(
            status_code=403,
            detail="Cannot associate token for another user's account"
        )

    result = await service.associate_ur_token(
        account_id=request.account_id,
        account_key=request.account_key
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data=result.metadata
    )


# ==================== CONVERSION ROUTES ====================

@router.post("/conversion/request", response_model=TransactionResponse)
async def request_conversion(
    request: ConversionRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Request conversion between UR and fiat currency.

    For UR -> Fiat: Tokens are locked, fiat is sent via payout method
    For Fiat -> UR: Payment is collected, UR tokens are minted/transferred
    """
    service = get_service()

    # Get current conversion rate (would come from liquidity pool)
    # Placeholder rates - in production, query from sovereign_economy tables
    rates = {
        'CAD': Decimal('1.35'),
        'USD': Decimal('1.00')
    }
    rate = rates.get(request.currency, Decimal('1.00'))

    user_account = user.get('hedera_account_id')

    if request.direction == 'ur_to_fiat':
        if not user_account:
            raise HTTPException(
                status_code=400,
                detail="User does not have a Hedera account"
            )

        # Verify balance
        success, balance, error = await service.get_ur_balance(user_account)
        if not success or balance < request.amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient UR balance for conversion"
            )

        # Calculate fiat amount
        fiat_amount = request.amount * rate

        # In production: Create conversion_request record in database,
        # lock tokens, initiate payout via Stripe/banking service

        return TransactionResponse(
            success=True,
            transaction_id=None,  # Will be set when conversion processes
            status="PENDING",
            data={
                'direction': 'ur_to_fiat',
                'ur_amount': str(request.amount),
                'fiat_amount': str(fiat_amount),
                'currency': request.currency,
                'rate': str(rate),
                'payout_method': request.payout_method,
                'estimated_completion': '24-48 hours'
            }
        )

    else:  # fiat_to_ur
        # Calculate UR amount
        ur_amount = request.amount / rate

        # In production: Create Stripe payment intent,
        # mint tokens on payment confirmation

        return TransactionResponse(
            success=True,
            transaction_id=None,
            status="AWAITING_PAYMENT",
            data={
                'direction': 'fiat_to_ur',
                'fiat_amount': str(request.amount),
                'ur_amount': str(ur_amount),
                'currency': request.currency,
                'rate': str(rate),
                'payment_url': '/api/payment/create'  # Placeholder
            }
        )


@router.get("/conversion/rate")
async def get_conversion_rate(
    currency: str = 'CAD',
    user: dict = Depends(get_current_user)
):
    """
    Get current UR conversion rate.
    """
    # In production, query from liquidity_pool table
    rates = {
        'CAD': {'rate': Decimal('1.35'), 'direction': '1 UR = 1.35 CAD'},
        'USD': {'rate': Decimal('1.00'), 'direction': '1 UR = 1.00 USD'}
    }

    if currency not in rates:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    return {
        'currency': currency,
        'rate': str(rates[currency]['rate']),
        'description': rates[currency]['direction'],
        'last_updated': datetime.utcnow().isoformat(),
        'source': 'liquidity_pool'
    }


# ==================== DASHBOARD ROUTES ====================

@router.get("/dashboard/economic", response_model=EconomicDashboardResponse)
async def get_economic_dashboard(
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(3))  # INITIATE+
):
    """
    Get comprehensive economic dashboard data.

    Includes token stats, liquidity info, conversion rates, and health indicators.
    """
    service = get_service()

    # Get token info
    token_info = await service.get_token_info()

    # In production, these would come from database queries
    ur_stats = {
        'total_supply': str(token_info.total_supply) if token_info else '0',
        'circulating': str(token_info.circulating_supply) if token_info else '0',
        'treasury': str(token_info.treasury_balance) if token_info else '0',
        'holders': 0,  # Would query from database
        'transactions_24h': 0
    }

    liquidity = {
        'fiat_cad': '0.00',
        'fiat_usd': '0.00',
        'reserve_ratio': '100%',
        'emergency_mode': False
    }

    conversion_rate = {
        'CAD': Decimal('1.35'),
        'USD': Decimal('1.00')
    }

    # Health indicators based on economic parameters
    health_indicators = {
        'liquidity_health': 'GOOD',
        'velocity': 'MODERATE',
        'distribution_gini': 0.35,  # Lower is more equal
        'reserve_status': 'ADEQUATE',
        'governance_participation': 0.65
    }

    return EconomicDashboardResponse(
        ur_stats=ur_stats,
        liquidity=liquidity,
        conversion_rate=conversion_rate,
        recent_activity=[],  # Would query recent transactions
        health_indicators=health_indicators
    )


@router.get("/dashboard/personal")
async def get_personal_dashboard(
    user: dict = Depends(get_current_user)
):
    """
    Get personal economic dashboard for the authenticated user.
    """
    service = get_service()
    user_account = user.get('hedera_account_id')

    balance_data = {
        'ur_balance': '0',
        'ur_locked': '0',
        'ur_pending': '0',
        'total_available': '0'
    }

    if user_account:
        success, balance, _ = await service.get_ur_balance(user_account)
        if success:
            balance_data['ur_balance'] = str(balance)
            balance_data['total_available'] = str(balance)

    return {
        'account_id': user_account,
        'balance': balance_data,
        'resonance_score': user.get('resonance_score', 0),
        'sovereignty_level': user.get('sovereignty_level', 1),
        'recent_transactions': [],  # Would query from database
        'pending_conversions': [],
        'rewards': {
            'referral_bonus': '0',
            'participation_bonus': '0',
            'staking_rewards': '0'
        }
    }


# ==================== ADMIN ROUTES ====================

@router.get("/admin/simulation-state")
async def get_simulation_state(
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(7))  # SOVEREIGN only
):
    """
    Get current simulation state (for testing/development).

    Only available when service is running in simulation mode.
    """
    service = get_service()
    state = service.get_simulation_state()

    if not state.get('simulation_mode'):
        raise HTTPException(
            status_code=400,
            detail="Service is not in simulation mode"
        )

    return state


@router.post("/admin/initialize-token", response_model=TransactionResponse)
async def initialize_ur_token(
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(7))  # SOVEREIGN only
):
    """
    Initialize the UR token on Hedera.

    This should only be called once during initial deployment.
    """
    service = get_service()

    # Check if token already exists
    token_info = await service.get_token_info()
    if token_info and token_info.token_id:
        raise HTTPException(
            status_code=400,
            detail="UR token already exists"
        )

    result = await service.create_ur_token(
        name="Unité de Résonance",
        symbol="UR",
        decimals=8,
        initial_supply=0
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data={
            'token_id': result.metadata.get('token_id'),
            'message': 'UR token created. Update HEDERA_UR_TOKEN_ID in environment.'
        }
    )


@router.post("/admin/create-hcs-topic", response_model=TransactionResponse)
async def create_hcs_topic(
    user: dict = Depends(get_current_user),
    _: None = Depends(require_sovereignty_level(7))  # SOVEREIGN only
):
    """
    Create HCS topic for audit logging.

    This should only be called once during initial deployment.
    """
    service = get_service()

    result = await service.create_audit_topic(
        memo="AT·OM Sovereign Economy Audit Log"
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)

    return TransactionResponse(
        success=True,
        transaction_id=result.transaction_id,
        status=result.receipt_status,
        data={
            'topic_id': result.metadata.get('topic_id'),
            'message': 'HCS topic created. Update HEDERA_HCS_TOPIC_ID in environment.'
        }
    )
