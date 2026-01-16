"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V75 — TOKENS API                                  ║
║                                                                              ║
║  Gestion des tokens internes (pas crypto) pour gouvernance                   ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/tokens", tags=["Tokens"])

# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class TokenType(str, Enum):
    COMPUTE = "compute"      # AI processing
    STORAGE = "storage"      # Data storage
    BANDWIDTH = "bandwidth"  # API calls
    AGENT = "agent"          # Agent operations

class TokenTransaction(BaseModel):
    id: str
    type: TokenType
    amount: int
    description: str
    agent_id: Optional[str] = None
    thread_id: Optional[str] = None
    created_at: datetime

class TokenBalance(BaseModel):
    total: int
    available: int
    reserved: int
    used_today: int
    daily_limit: int
    breakdown: dict[TokenType, int]

class TokenUsageStats(BaseModel):
    period: str
    total_used: int
    by_type: dict[TokenType, int]
    by_agent: dict[str, int]
    by_sphere: dict[str, int]

# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

USER_BALANCE = TokenBalance(
    total=100000,
    available=85000,
    reserved=5000,
    used_today=10000,
    daily_limit=50000,
    breakdown={
        TokenType.COMPUTE: 60000,
        TokenType.STORAGE: 20000,
        TokenType.BANDWIDTH: 15000,
        TokenType.AGENT: 5000,
    }
)

TRANSACTIONS: List[TokenTransaction] = [
    TokenTransaction(
        id="tx-001",
        type=TokenType.COMPUTE,
        amount=-500,
        description="Nova chat query processing",
        thread_id="thread-1",
        created_at=datetime.utcnow() - timedelta(minutes=30),
    ),
    TokenTransaction(
        id="tx-002",
        type=TokenType.AGENT,
        amount=-200,
        description="Agent task execution",
        agent_id="agent-research",
        thread_id="thread-1",
        created_at=datetime.utcnow() - timedelta(hours=1),
    ),
    TokenTransaction(
        id="tx-003",
        type=TokenType.STORAGE,
        amount=-100,
        description="File upload storage",
        created_at=datetime.utcnow() - timedelta(hours=2),
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/balance", response_model=TokenBalance)
async def get_balance():
    """Get current token balance."""
    return USER_BALANCE

@router.get("/transactions", response_model=List[TokenTransaction])
async def list_transactions(
    limit: int = Query(default=20, le=100),
    type: Optional[TokenType] = None,
    thread_id: Optional[str] = None,
):
    """List token transactions."""
    results = TRANSACTIONS.copy()
    
    if type:
        results = [t for t in results if t.type == type]
    if thread_id:
        results = [t for t in results if t.thread_id == thread_id]
    
    results.sort(key=lambda x: x.created_at, reverse=True)
    return results[:limit]

@router.get("/usage", response_model=TokenUsageStats)
async def get_usage_stats(period: str = Query(default="today", pattern="^(today|week|month)$")):
    """Get token usage statistics."""
    return TokenUsageStats(
        period=period,
        total_used=10000 if period == "today" else 50000 if period == "week" else 150000,
        by_type={
            TokenType.COMPUTE: 6000,
            TokenType.STORAGE: 2000,
            TokenType.BANDWIDTH: 1500,
            TokenType.AGENT: 500,
        },
        by_agent={
            "agent-research": 2000,
            "agent-writer": 1500,
            "agent-analyst": 1000,
        },
        by_sphere={
            "personal": 3000,
            "business": 4000,
            "creative": 2000,
            "scholar": 1000,
        },
    )

@router.post("/reserve")
async def reserve_tokens(amount: int, reason: str):
    """Reserve tokens for an operation (governance checkpoint)."""
    if amount > USER_BALANCE.available:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient tokens. Available: {USER_BALANCE.available}, Requested: {amount}"
        )
    
    return {
        "success": True,
        "reservation_id": f"res-{uuid4().hex[:8]}",
        "amount": amount,
        "reason": reason,
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }

@router.get("/limits")
async def get_limits():
    """Get token limits and quotas."""
    return {
        "daily_limit": 50000,
        "monthly_limit": 1000000,
        "per_query_max": 5000,
        "per_agent_max": 2000,
        "reserved_buffer": 5000,
    }
