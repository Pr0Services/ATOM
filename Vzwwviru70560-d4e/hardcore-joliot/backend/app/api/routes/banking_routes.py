"""
CHE·NU Canadian Banking API Routes V72

REST endpoints for Canadian banking integrations:
- Bank connection management
- Account operations
- Transaction queries
- Analytics and summaries

@version V72.0
@phase Phase 2 - Financial Integrations
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from pydantic import BaseModel, Field

from app.services.canadian_banking_service import (
    canadian_banking_service,
    CanadianBank,
    BankConnectionStatus,
    AccountType,
    TransactionCategory,
    BankAccount,
    BankTransaction,
    BankConnection,
)


router = APIRouter(prefix="/api/v2/banking", tags=["Canadian Banking"])


# ==============================================================================
# SCHEMAS
# ==============================================================================

class BankInfo(BaseModel):
    """Bank information response."""
    id: str
    name: str
    name_fr: str
    icon: str
    color: str
    mfa_required: bool


class ConnectionInitRequest(BaseModel):
    """Request to initiate bank connection."""
    bank_id: str = Field(..., description="Bank identifier (e.g., 'desjardins', 'td_bank')")
    redirect_uri: Optional[str] = Field(None, description="Custom redirect URI after auth")


class ConnectionInitResponse(BaseModel):
    """Response with connection iframe URL."""
    iframe_url: str
    state: str
    expires_in: int = 900  # 15 minutes


class ConnectionCompleteRequest(BaseModel):
    """Request to complete bank connection after callback."""
    state: str
    login_id: str
    institution: str


class BankAccountResponse(BaseModel):
    """Bank account response."""
    id: str
    bank_id: str
    account_number_masked: str
    account_type: str
    currency: str
    balance: float
    available_balance: float
    account_name: str
    institution_name: str
    last_refreshed: datetime

    class Config:
        from_attributes = True


class BankTransactionResponse(BaseModel):
    """Bank transaction response."""
    id: str
    account_id: str
    date: datetime
    description: str
    amount: float
    currency: str
    category: str
    merchant: Optional[str]
    pending: bool

    class Config:
        from_attributes = True


class BankConnectionResponse(BaseModel):
    """Bank connection response."""
    id: str
    bank_id: str
    status: str
    last_sync: Optional[datetime]
    accounts_count: int
    created_at: datetime
    error_message: Optional[str]

    class Config:
        from_attributes = True


class AccountSummaryResponse(BaseModel):
    """Account summary response."""
    total_accounts: int
    connected_banks: int
    total_balance: Dict[str, float]
    by_account_type: Dict[str, Dict[str, Any]]
    by_bank: Dict[str, Dict[str, Any]]


class SpendingByCategoryResponse(BaseModel):
    """Spending by category response."""
    period_start: datetime
    period_end: datetime
    spending: Dict[str, float]
    total: float


class DisconnectRequest(BaseModel):
    """Request to disconnect bank."""
    connection_id: str


# ==============================================================================
# HELPER - Get User ID (Mock for now, integrate with auth)
# ==============================================================================

def get_current_user_id(request: Request) -> str:
    """
    Get current user ID from request.
    In production, this would verify JWT and extract user_id.
    """
    # Mock user ID for development
    # In production: decode JWT from Authorization header
    user_id = request.headers.get("X-User-Id", "demo-user-123")
    return user_id


# ==============================================================================
# HEALTH & INFO
# ==============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint for banking service."""
    return {
        "status": "healthy",
        "service": "CHE-NU Canadian Banking Service",
        "version": "72.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/banks", response_model=List[BankInfo])
async def list_supported_banks():
    """
    List all supported Canadian banks.

    Returns information about each bank including name,
    French name, icon, color, and MFA requirements.
    """
    return canadian_banking_service.get_supported_banks()


@router.get("/banks/{bank_id}", response_model=BankInfo)
async def get_bank_info(bank_id: str):
    """Get information about a specific bank."""
    try:
        bank_enum = CanadianBank(bank_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank '{bank_id}' not found"
        )

    config = canadian_banking_service.get_bank_config(bank_enum)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank '{bank_id}' configuration not found"
        )

    return BankInfo(
        id=config.bank_id.value,
        name=config.name,
        name_fr=config.name_fr,
        icon=config.icon,
        color=config.color,
        mfa_required=config.mfa_required
    )


# ==============================================================================
# CONNECTION FLOW
# ==============================================================================

@router.post("/connect", response_model=ConnectionInitResponse)
async def initiate_connection(
    data: ConnectionInitRequest,
    request: Request
):
    """
    Initiate bank connection flow.

    Returns an iframe URL to embed in the frontend for secure
    credential entry via Flinks. The state parameter should be
    stored and verified in the callback.
    """
    user_id = get_current_user_id(request)

    try:
        bank_enum = CanadianBank(data.bank_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid bank_id: {data.bank_id}"
        )

    try:
        iframe_url, state = canadian_banking_service.initiate_connection(
            user_id=user_id,
            bank_id=bank_enum,
            redirect_uri=data.redirect_uri
        )

        return ConnectionInitResponse(
            iframe_url=iframe_url,
            state=state,
            expires_in=900  # 15 minutes
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/connect/complete", response_model=BankConnectionResponse)
async def complete_connection(
    data: ConnectionCompleteRequest,
    request: Request
):
    """
    Complete bank connection after Flinks callback.

    Called after user completes authentication in the Flinks iframe.
    The state, login_id, and institution are provided by the callback.
    """
    try:
        connection = canadian_banking_service.complete_connection(
            state=data.state,
            login_id=data.login_id,
            institution=data.institution
        )

        return BankConnectionResponse(
            id=connection.id,
            bank_id=connection.bank_id.value,
            status=connection.status.value,
            last_sync=connection.last_sync,
            accounts_count=len(connection.accounts),
            created_at=connection.created_at,
            error_message=connection.error_message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/disconnect")
async def disconnect_bank(
    data: DisconnectRequest,
    request: Request
):
    """
    Disconnect a bank connection.

    Removes the connection and all associated account data.
    This action cannot be undone.
    """
    user_id = get_current_user_id(request)

    success = canadian_banking_service.disconnect_bank(
        user_id=user_id,
        connection_id=data.connection_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found or access denied"
        )

    return {"status": "disconnected", "connection_id": data.connection_id}


# ==============================================================================
# CONNECTIONS
# ==============================================================================

@router.get("/connections", response_model=List[BankConnectionResponse])
async def list_connections(request: Request):
    """List all bank connections for the current user."""
    user_id = get_current_user_id(request)

    connections = canadian_banking_service.get_connections(user_id)

    return [
        BankConnectionResponse(
            id=conn.id,
            bank_id=conn.bank_id.value,
            status=conn.status.value,
            last_sync=conn.last_sync,
            accounts_count=len(conn.accounts),
            created_at=conn.created_at,
            error_message=conn.error_message
        )
        for conn in connections
    ]


@router.get("/connections/{connection_id}", response_model=BankConnectionResponse)
async def get_connection(
    connection_id: str,
    request: Request
):
    """Get details of a specific bank connection."""
    user_id = get_current_user_id(request)

    connection = canadian_banking_service.get_connection(connection_id)

    if not connection or connection.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )

    return BankConnectionResponse(
        id=connection.id,
        bank_id=connection.bank_id.value,
        status=connection.status.value,
        last_sync=connection.last_sync,
        accounts_count=len(connection.accounts),
        created_at=connection.created_at,
        error_message=connection.error_message
    )


# ==============================================================================
# ACCOUNTS
# ==============================================================================

@router.get("/accounts", response_model=List[BankAccountResponse])
async def list_accounts(
    request: Request,
    bank_id: Optional[str] = Query(None, description="Filter by bank"),
    account_type: Optional[str] = Query(None, description="Filter by account type")
):
    """
    List all bank accounts for the current user.

    Optionally filter by bank or account type.
    """
    user_id = get_current_user_id(request)

    accounts = canadian_banking_service.get_accounts(user_id)

    # Apply filters
    if bank_id:
        accounts = [a for a in accounts if a.bank_id.value == bank_id]

    if account_type:
        accounts = [a for a in accounts if a.account_type.value == account_type]

    return [
        BankAccountResponse(
            id=acc.id,
            bank_id=acc.bank_id.value,
            account_number_masked=acc.account_number_masked,
            account_type=acc.account_type.value,
            currency=acc.currency,
            balance=acc.balance,
            available_balance=acc.available_balance,
            account_name=acc.account_name,
            institution_name=acc.institution_name,
            last_refreshed=acc.last_refreshed
        )
        for acc in accounts
    ]


@router.get("/accounts/{account_id}", response_model=BankAccountResponse)
async def get_account(
    account_id: str,
    request: Request
):
    """Get details of a specific bank account."""
    user_id = get_current_user_id(request)

    account = canadian_banking_service.get_account(account_id)

    if not account or account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    return BankAccountResponse(
        id=account.id,
        bank_id=account.bank_id.value,
        account_number_masked=account.account_number_masked,
        account_type=account.account_type.value,
        currency=account.currency,
        balance=account.balance,
        available_balance=account.available_balance,
        account_name=account.account_name,
        institution_name=account.institution_name,
        last_refreshed=account.last_refreshed
    )


@router.post("/accounts/refresh", response_model=List[BankAccountResponse])
async def refresh_accounts(request: Request):
    """
    Refresh all account data from connected banks.

    Fetches the latest balance and account information.
    """
    user_id = get_current_user_id(request)

    accounts = canadian_banking_service.refresh_accounts(user_id)

    return [
        BankAccountResponse(
            id=acc.id,
            bank_id=acc.bank_id.value,
            account_number_masked=acc.account_number_masked,
            account_type=acc.account_type.value,
            currency=acc.currency,
            balance=acc.balance,
            available_balance=acc.available_balance,
            account_name=acc.account_name,
            institution_name=acc.institution_name,
            last_refreshed=acc.last_refreshed
        )
        for acc in accounts
    ]


# ==============================================================================
# TRANSACTIONS
# ==============================================================================

@router.get("/accounts/{account_id}/transactions", response_model=List[BankTransactionResponse])
async def get_account_transactions(
    account_id: str,
    request: Request,
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of transactions")
):
    """
    Get transactions for a specific account.

    Supports filtering by date range and category.
    """
    user_id = get_current_user_id(request)

    # Verify account access
    account = canadian_banking_service.get_account(account_id)
    if not account or account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    transactions = canadian_banking_service.get_transactions(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

    # Apply category filter
    if category:
        transactions = [t for t in transactions if t.category.value == category]

    return [
        BankTransactionResponse(
            id=tx.id,
            account_id=tx.account_id,
            date=tx.date,
            description=tx.description,
            amount=tx.amount,
            currency=tx.currency,
            category=tx.category.value,
            merchant=tx.merchant,
            pending=tx.pending
        )
        for tx in transactions
    ]


@router.get("/transactions/recent", response_model=List[BankTransactionResponse])
async def get_recent_transactions(
    request: Request,
    limit: int = Query(20, ge=1, le=100, description="Number of transactions")
):
    """
    Get recent transactions across all accounts.

    Returns the most recent transactions sorted by date.
    """
    user_id = get_current_user_id(request)

    transactions = canadian_banking_service.get_recent_transactions(
        user_id=user_id,
        limit=limit
    )

    return [
        BankTransactionResponse(
            id=tx.id,
            account_id=tx.account_id,
            date=tx.date,
            description=tx.description,
            amount=tx.amount,
            currency=tx.currency,
            category=tx.category.value,
            merchant=tx.merchant,
            pending=tx.pending
        )
        for tx in transactions
    ]


# ==============================================================================
# ANALYTICS
# ==============================================================================

@router.get("/summary", response_model=AccountSummaryResponse)
async def get_account_summary(request: Request):
    """
    Get summary of all connected accounts.

    Includes total balances by currency, breakdown by account type,
    and breakdown by bank.
    """
    user_id = get_current_user_id(request)

    summary = canadian_banking_service.get_account_summary(user_id)

    return AccountSummaryResponse(**summary)


@router.get("/spending", response_model=SpendingByCategoryResponse)
async def get_spending_by_category(
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get spending breakdown by category.

    Analyzes transactions over the specified period and groups
    spending by category.
    """
    user_id = get_current_user_id(request)

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    spending = canadian_banking_service.get_spending_by_category(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return SpendingByCategoryResponse(
        period_start=start_date,
        period_end=end_date,
        spending=spending,
        total=sum(spending.values())
    )


@router.get("/balance/total")
async def get_total_balance(request: Request):
    """
    Get total balance across all connected accounts.

    Returns balance grouped by currency.
    """
    user_id = get_current_user_id(request)

    totals = canadian_banking_service.get_total_balance(user_id)

    return {
        "balances": totals,
        "primary_currency": "CAD",
        "timestamp": datetime.utcnow().isoformat()
    }
