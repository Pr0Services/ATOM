"""
AT·OM — Tokenomics Engine
===========================

Core economic service for the AT·OM sovereign economy.
Handles multi-instrument operations and state management.

Author: AT·OM Collective
"""

from __future__ import annotations

import logging
import math
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List, Tuple
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

logger = logging.getLogger("nova999.tokenomics")


# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class TokenType(Enum):
    UR = "UR"           # Unité de Résonance (stable)
    JT = "JT"           # Jeton de Transition (pre-launch)
    ATOM = "ATOM"       # Bonding Curve crypto
    FLOW = "FLOW"       # Flow Keeper souvenir token


class NFTTier(Enum):
    GRAINE = "graine"
    POUSSE = "pousse"
    BRANCHE = "branche"
    RACINE = "racine"
    ARBRE = "arbre"


class JTTier(Enum):
    ETINCELLE = "etincelle"   # $25+
    FLAMME = "flamme"         # $100+
    FEU = "feu"               # $500+
    BRASIER = "brasier"       # $2,000+
    SOLEIL = "soleil"         # $10,000+


class FlowType(Enum):
    TECH = "tech"
    VIE = "vie"
    SAGESSE = "sagesse"
    JUSTICE = "justice"
    GRAINE = "graine"
    TERRE = "terre"


class FundCategory(Enum):
    DEVELOPMENT = "development"       # 40%
    STIMULATION = "stimulation"       # 30%
    STRUCTURE = "structure"           # 20%
    EMERGENCY = "emergency"           # 10%


# ─── NFT Configuration ───────────────────────────────────────────────────────

NFT_CONFIG: Dict[NFTTier, Dict[str, Any]] = {
    NFTTier.GRAINE: {
        "name": "Graine de l'Arche",
        "min_contribution": Decimal("10"),
        "max_contribution": Decimal("99.99"),
        "max_supply": None,  # Unlimited during Phase I
        "ur_bonus_pct": Decimal("0"),
        "symbol": "🌰",
        "frequency_hz": 111,
        "utilities": ["early_access", "badge"],
    },
    NFTTier.POUSSE: {
        "name": "Pousse de l'Arbre",
        "min_contribution": Decimal("100"),
        "max_contribution": Decimal("499.99"),
        "max_supply": 1000,
        "ur_bonus_pct": Decimal("5"),
        "symbol": "🌱",
        "frequency_hz": 222,
        "utilities": ["early_access", "badge", "ur_bonus_5", "founder_channel_read"],
    },
    NFTTier.BRANCHE: {
        "name": "Branche de l'Arbre de Vie",
        "min_contribution": Decimal("500"),
        "max_contribution": Decimal("1999.99"),
        "max_supply": 144,
        "ur_bonus_pct": Decimal("15"),
        "symbol": "🌿",
        "frequency_hz": 333,
        "utilities": ["early_access", "badge", "ur_bonus_15", "consultative_vote",
                       "early_features", "monthly_call"],
    },
    NFTTier.RACINE: {
        "name": "Racine de l'Arche",
        "min_contribution": Decimal("2000"),
        "max_contribution": Decimal("9999.99"),
        "max_supply": 36,
        "ur_bonus_pct": Decimal("30"),
        "symbol": "🌳",
        "frequency_hz": 444,
        "utilities": ["early_access", "badge", "ur_bonus_30", "revenue_share",
                       "advisory_council", "evolving_nft"],
    },
    NFTTier.ARBRE: {
        "name": "Arbre de Vie Complet",
        "min_contribution": Decimal("10000"),
        "max_contribution": None,  # No upper limit
        "max_supply": 9,
        "ur_bonus_pct": Decimal("50"),
        "symbol": "🌲",
        "frequency_hz": 999,
        "utilities": ["early_access", "badge", "ur_bonus_50", "revenue_share",
                       "advisory_council", "evolving_nft", "architect_founder",
                       "governance_2x", "sphere_revenue_01pct", "founder_direct_line",
                       "name_in_source_code"],
    },
}

# ─── JT Configuration ────────────────────────────────────────────────────────

JT_CONFIG: Dict[JTTier, Dict[str, Any]] = {
    JTTier.ETINCELLE: {
        "name": "Étincelle",
        "min_usd": Decimal("25"),
        "jt_bonus_pct": Decimal("0"),
        "nft_tier": None,
        "symbol": "✨",
    },
    JTTier.FLAMME: {
        "name": "Flamme",
        "min_usd": Decimal("100"),
        "jt_bonus_pct": Decimal("5"),
        "nft_tier": NFTTier.GRAINE,
        "symbol": "🕯️",
    },
    JTTier.FEU: {
        "name": "Feu",
        "min_usd": Decimal("500"),
        "jt_bonus_pct": Decimal("10"),
        "nft_tier": NFTTier.BRANCHE,
        "symbol": "🔥",
    },
    JTTier.BRASIER: {
        "name": "Brasier",
        "min_usd": Decimal("2000"),
        "jt_bonus_pct": Decimal("15"),
        "nft_tier": NFTTier.RACINE,
        "symbol": "🔥",
    },
    JTTier.SOLEIL: {
        "name": "Soleil",
        "min_usd": Decimal("10000"),
        "jt_bonus_pct": Decimal("20"),
        "nft_tier": NFTTier.ARBRE,
        "symbol": "☀️",
    },
}

# ─── Fund Allocation ─────────────────────────────────────────────────────────

FUND_ALLOCATION = {
    FundCategory.DEVELOPMENT: Decimal("0.40"),
    FundCategory.STIMULATION: Decimal("0.30"),
    FundCategory.STRUCTURE: Decimal("0.20"),
    FundCategory.EMERGENCY: Decimal("0.10"),
}

# ─── Bonding Curve Configuration ──────────────────────────────────────────────

BONDING_CURVE_CONFIG = {
    "base_price": Decimal("0.01"),       # Initial price: $0.01 per ATOM
    "scale_factor": Decimal("100000"),   # Supply at which price doubles
    "exponent": Decimal("0.5"),          # Square root curve (gentle)
    "reserve_ratio": Decimal("0.50"),    # 50% of buy price goes to reserve
    "genesis_supply": Decimal("999000"), # Initial supply (999 × 1000)
    "max_supply": Decimal("9990000"),    # Max 9,990,000 ATOM (999 × 10,000)
    "symbol": "ATOM",
    "name": "AT·OM Token",
}

# ─── JT → UR Conversion Rates (by seniority) ─────────────────────────────────

JT_CONVERSION_RATES = {
    "6_months_plus": Decimal("1.5"),   # 6+ months before launch → 1 JT = 1.5 UR
    "3_to_6_months": Decimal("1.3"),   # 3-6 months → 1 JT = 1.3 UR
    "0_to_3_months": Decimal("1.1"),   # 0-3 months → 1 JT = 1.1 UR
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ContributionResult:
    """Result of processing a contribution."""
    success: bool
    contributor_id: str
    amount_usd: Decimal
    jt_tier: JTTier
    jt_minted: Decimal
    nft_tier: Optional[NFTTier]
    nft_serial: Optional[int]
    flow_token_id: Optional[str]
    fund_allocation: Dict[str, Decimal]
    hedera_tx_id: Optional[str] = None
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, Decimal):
                d[k] = str(v)
        return d


@dataclass
class BondingCurveQuote:
    """Quote for buying/selling ATOM tokens."""
    action: str  # "buy" or "sell"
    amount_tokens: Decimal
    price_per_token: Decimal
    total_cost: Decimal
    to_reserve: Decimal
    new_supply: Decimal
    new_price: Decimal
    slippage_pct: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {k: str(v) if isinstance(v, Decimal) else v for k, v in asdict(self).items()}


@dataclass
class TokenEconomyState:
    """Current state of the entire token economy."""
    # UR
    ur_total_supply: Decimal = Decimal("0")
    ur_circulating: Decimal = Decimal("0")
    ur_treasury: Decimal = Decimal("0")

    # JT
    jt_total_minted: Decimal = Decimal("0")
    jt_total_converted: Decimal = Decimal("0")
    jt_outstanding: Decimal = Decimal("0")

    # ATOM (Bonding Curve)
    atom_supply: Decimal = Decimal("0")
    atom_price: Decimal = Decimal("0.01")
    atom_reserve: Decimal = Decimal("0")
    atom_market_cap: Decimal = Decimal("0")

    # NFT
    nft_minted: Dict[str, int] = field(default_factory=lambda: {
        t.value: 0 for t in NFTTier
    })

    # Funds
    total_raised_usd: Decimal = Decimal("0")
    fund_balances: Dict[str, Decimal] = field(default_factory=lambda: {
        c.value: Decimal("0") for c in FundCategory
    })

    # Flow Keeper
    flow_total: Decimal = Decimal("0")
    flow_by_type: Dict[str, Decimal] = field(default_factory=lambda: {
        f.value: Decimal("0") for f in FlowType
    })
    flow_token_count: int = 0

    # Stats
    total_contributors: int = 0
    launch_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Convert all Decimal to str for JSON
        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return str(obj)
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj
        return convert(d)


# =============================================================================
# BONDING CURVE ENGINE
# =============================================================================

class BondingCurveEngine:
    """
    Bonding Curve for the ATOM token.

    Price formula: price = base_price × (1 + supply / scale_factor) ^ exponent

    This creates a SQUARE ROOT curve (exponent=0.5):
    - At supply 0:       price = $0.01
    - At supply 100,000: price = $0.0141 (√2 × base)
    - At supply 500,000: price = $0.0245
    - At supply 999,000: price = $0.0332 (genesis price)
    - At supply 9,990,000: price = $0.1048 (max supply price)

    Why this curve:
    - GENTLE growth: not exponential, not flat
    - Early supporters get lower prices (reward)
    - Late joiners still get fair prices (not exploitative)
    - Reserve ensures liquidity for exits
    - Aligned with "Circulation > Accumulation"
    """

    def __init__(self, config: Optional[Dict] = None):
        cfg = config or BONDING_CURVE_CONFIG
        self.base_price = cfg["base_price"]
        self.scale_factor = cfg["scale_factor"]
        self.exponent = cfg["exponent"]
        self.reserve_ratio = cfg["reserve_ratio"]
        self.max_supply = cfg["max_supply"]

        # State
        self.current_supply = Decimal("0")
        self.reserve_balance = Decimal("0")

    def price_at_supply(self, supply: Decimal) -> Decimal:
        """Calculate token price at a given supply level."""
        if supply <= 0:
            return self.base_price
        ratio = float(supply / self.scale_factor)
        multiplier = (1 + ratio) ** float(self.exponent)
        return (self.base_price * Decimal(str(multiplier))).quantize(
            Decimal("0.000001"), rounding=ROUND_HALF_UP
        )

    def current_price(self) -> Decimal:
        """Get current token price."""
        return self.price_at_supply(self.current_supply)

    def quote_buy(self, amount_tokens: Decimal) -> BondingCurveQuote:
        """
        Get a quote for buying tokens.
        Uses integral of the curve for accurate pricing.
        """
        if self.current_supply + amount_tokens > self.max_supply:
            remaining = self.max_supply - self.current_supply
            raise ValueError(
                f"Cannot buy {amount_tokens} ATOM. Max remaining: {remaining}"
            )

        # Calculate cost using average of start and end price (trapezoidal)
        start_price = self.price_at_supply(self.current_supply)
        end_price = self.price_at_supply(self.current_supply + amount_tokens)
        avg_price = (start_price + end_price) / 2
        total_cost = (avg_price * amount_tokens).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        to_reserve = (total_cost * self.reserve_ratio).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        new_supply = self.current_supply + amount_tokens
        slippage = ((end_price - start_price) / start_price * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ) if start_price > 0 else Decimal("0")

        return BondingCurveQuote(
            action="buy",
            amount_tokens=amount_tokens,
            price_per_token=avg_price,
            total_cost=total_cost,
            to_reserve=to_reserve,
            new_supply=new_supply,
            new_price=end_price,
            slippage_pct=slippage,
        )

    def quote_sell(self, amount_tokens: Decimal) -> BondingCurveQuote:
        """
        Get a quote for selling tokens.
        Sell price comes from the reserve.
        """
        if amount_tokens > self.current_supply:
            raise ValueError(
                f"Cannot sell {amount_tokens} ATOM. Current supply: {self.current_supply}"
            )

        start_price = self.price_at_supply(self.current_supply)
        end_price = self.price_at_supply(self.current_supply - amount_tokens)
        avg_price = (start_price + end_price) / 2

        # Sell payout comes from reserve (slightly less than buy price)
        total_payout = (avg_price * amount_tokens * self.reserve_ratio).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        # Cap at available reserve
        total_payout = min(total_payout, self.reserve_balance)

        new_supply = self.current_supply - amount_tokens

        return BondingCurveQuote(
            action="sell",
            amount_tokens=amount_tokens,
            price_per_token=avg_price,
            total_cost=total_payout,
            to_reserve=Decimal("0") - total_payout,
            new_supply=new_supply,
            new_price=end_price,
            slippage_pct=Decimal("0"),
        )

    def execute_buy(self, amount_tokens: Decimal) -> BondingCurveQuote:
        """Execute a buy order."""
        quote = self.quote_buy(amount_tokens)
        self.current_supply += amount_tokens
        self.reserve_balance += quote.to_reserve
        logger.info(
            f"ATOM BUY: {amount_tokens} tokens @ ${quote.price_per_token} "
            f"= ${quote.total_cost} (reserve: ${self.reserve_balance})"
        )
        return quote

    def execute_sell(self, amount_tokens: Decimal) -> BondingCurveQuote:
        """Execute a sell order."""
        quote = self.quote_sell(amount_tokens)
        self.current_supply -= amount_tokens
        self.reserve_balance -= abs(quote.to_reserve)
        logger.info(
            f"ATOM SELL: {amount_tokens} tokens @ ${quote.price_per_token} "
            f"= ${quote.total_cost} payout (reserve: ${self.reserve_balance})"
        )
        return quote

    def get_state(self) -> Dict[str, Any]:
        """Get current bonding curve state."""
        price = self.current_price()
        return {
            "supply": str(self.current_supply),
            "max_supply": str(self.max_supply),
            "price": str(price),
            "reserve": str(self.reserve_balance),
            "market_cap": str(price * self.current_supply),
            "reserve_ratio": str(self.reserve_ratio),
            "supply_pct": str(
                (self.current_supply / self.max_supply * 100).quantize(Decimal("0.01"))
            ) if self.max_supply > 0 else "0",
        }


# =============================================================================
# TOKENOMICS SERVICE (Main Orchestrator)
# =============================================================================

class TokenomicsService:
    """
    Central tokenomics orchestrator for AT·OM.

    Manages all 4 instruments (UR, JT, NFT, ATOM) and their interactions.
    """

    def __init__(self, launch_date: Optional[str] = None):
        self.state = TokenEconomyState()
        self.state.launch_date = launch_date
        self.bonding_curve = BondingCurveEngine()
        self._contribution_history: List[Dict[str, Any]] = []
        self._flow_history: List[Dict[str, Any]] = []
        self._next_flow_token_id = 1

        # Database bridge (Supabase persistence)
        try:
            try:
                from services.tokenomics_db import get_tokenomics_db
            except ImportError:
                from backend.services.tokenomics_db import get_tokenomics_db
            self.db = get_tokenomics_db()
            logger.info(f"TokenomicsService: DB bridge {'connected' if self.db.is_connected else 'in-memory mode'}")
        except ImportError:
            self.db = None
            logger.warning("TokenomicsService: DB bridge not available, using in-memory only")

    # ─── JT TIER DETERMINATION ────────────────────────────────────────────────

    @staticmethod
    def determine_jt_tier(amount_usd: Decimal) -> Optional[JTTier]:
        """Determine JT tier based on USD amount."""
        if amount_usd >= Decimal("10000"):
            return JTTier.SOLEIL
        elif amount_usd >= Decimal("2000"):
            return JTTier.BRASIER
        elif amount_usd >= Decimal("500"):
            return JTTier.FEU
        elif amount_usd >= Decimal("100"):
            return JTTier.FLAMME
        elif amount_usd >= Decimal("25"):
            return JTTier.ETINCELLE
        return None

    @staticmethod
    def determine_nft_tier(amount_usd: Decimal) -> Optional[NFTTier]:
        """Determine NFT tier based on USD amount."""
        if amount_usd >= Decimal("10000"):
            return NFTTier.ARBRE
        elif amount_usd >= Decimal("2000"):
            return NFTTier.RACINE
        elif amount_usd >= Decimal("500"):
            return NFTTier.BRANCHE
        elif amount_usd >= Decimal("100"):
            return NFTTier.POUSSE
        elif amount_usd >= Decimal("10"):
            return NFTTier.GRAINE
        return None

    # ─── CONTRIBUTION PROCESSING ──────────────────────────────────────────────

    def process_contribution(
        self,
        contributor_id: str,
        amount_usd: Decimal,
        flow_type: Optional[FlowType] = None,
        message: Optional[str] = None,
    ) -> ContributionResult:
        """
        Process a complete contribution.

        This is the MAIN entry point for when someone contributes money.
        It handles:
        1. JT minting (with tier bonus)
        2. NFT minting (if tier qualifies)
        3. Flow Token generation
        4. Fund allocation (40/30/20/10)
        5. State update

        Args:
            contributor_id: Unique ID of the contributor
            amount_usd: Amount contributed in USD
            flow_type: Optional preferred flow direction
            message: Optional personal message to engrave

        Returns:
            ContributionResult with all details
        """
        # Validate
        jt_tier = self.determine_jt_tier(amount_usd)
        if jt_tier is None:
            return ContributionResult(
                success=False,
                contributor_id=contributor_id,
                amount_usd=amount_usd,
                jt_tier=JTTier.ETINCELLE,
                jt_minted=Decimal("0"),
                nft_tier=None,
                nft_serial=None,
                flow_token_id=None,
                fund_allocation={},
                error="Minimum contribution is $25 USD",
            )

        jt_config = JT_CONFIG[jt_tier]
        bonus_pct = jt_config["jt_bonus_pct"]
        jt_amount = amount_usd * (1 + bonus_pct / 100)
        jt_amount = jt_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # NFT
        nft_tier = self.determine_nft_tier(amount_usd)
        nft_serial = None
        if nft_tier:
            nft_config = NFT_CONFIG[nft_tier]
            max_supply = nft_config["max_supply"]
            current_minted = self.state.nft_minted.get(nft_tier.value, 0)

            if max_supply is not None and current_minted >= max_supply:
                nft_tier = None  # Sold out — no NFT but contribution still valid
            else:
                nft_serial = current_minted + 1
                self.state.nft_minted[nft_tier.value] = nft_serial

        # Flow Token
        flow_token_id = None
        if flow_type:
            flow_token_id = f"FLOW-{flow_type.value.upper()}-{datetime.now(timezone.utc).strftime('%Y-%m%d')}-{self._next_flow_token_id:05d}"
            self._next_flow_token_id += 1
            self.state.flow_total += amount_usd
            self.state.flow_by_type[flow_type.value] = (
                self.state.flow_by_type.get(flow_type.value, Decimal("0")) + amount_usd
            )
            self.state.flow_token_count += 1

        # Fund allocation
        fund_alloc = {}
        for cat, pct in FUND_ALLOCATION.items():
            alloc = (amount_usd * pct).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            fund_alloc[cat.value] = alloc
            self.state.fund_balances[cat.value] = (
                self.state.fund_balances.get(cat.value, Decimal("0")) + alloc
            )

        # Update state
        self.state.jt_total_minted += jt_amount
        self.state.jt_outstanding += jt_amount
        self.state.total_raised_usd += amount_usd
        self.state.total_contributors += 1

        result = ContributionResult(
            success=True,
            contributor_id=contributor_id,
            amount_usd=amount_usd,
            jt_tier=jt_tier,
            jt_minted=jt_amount,
            nft_tier=nft_tier,
            nft_serial=nft_serial,
            flow_token_id=flow_token_id,
            fund_allocation=fund_alloc,
        )

        self._contribution_history.append(result.to_dict())
        logger.info(
            f"Contribution: {contributor_id} ${amount_usd} → "
            f"{jt_amount} JT ({jt_tier.value}), "
            f"NFT: {nft_tier.value if nft_tier else 'none'}"
        )

        # Persist to Supabase (async fire-and-forget)
        if self.db and self.db.is_connected:
            try:
                import asyncio
                db_data = {
                    "contributor_id": contributor_id,
                    "amount_usd": amount_usd,
                    "jt_tier": jt_tier.value,
                    "jt_minted": jt_amount,
                    "jt_bonus_pct": float(bonus_pct),
                    "nft_tier": nft_tier.value if nft_tier else None,
                    "nft_serial": nft_serial,
                    "flow_token_id": flow_token_id,
                    "flow_type": flow_type.value if flow_type else None,
                    "fund_development": float(fund_alloc.get("development", 0)),
                    "fund_stimulation": float(fund_alloc.get("stimulation", 0)),
                    "fund_structure": float(fund_alloc.get("structure", 0)),
                    "fund_emergency": float(fund_alloc.get("emergency", 0)),
                    "message": message,
                }
                asyncio.create_task(self.db.save_contribution(db_data))
            except Exception as e:
                logger.warning(f"DB persist failed (non-blocking): {e}")

        return result

    # ─── JT → UR CONVERSION ──────────────────────────────────────────────────

    def convert_jt_to_ur(
        self,
        contributor_id: str,
        jt_amount: Decimal,
        contribution_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convert Jetons de Transition to Unités de Résonance.

        Conversion rate depends on seniority (time between contribution and launch).

        Args:
            contributor_id: Who is converting
            jt_amount: Amount of JT to convert
            contribution_date: ISO date of original contribution

        Returns:
            Dict with conversion details
        """
        if jt_amount > self.state.jt_outstanding:
            return {
                "success": False,
                "error": f"Not enough JT outstanding. Available: {self.state.jt_outstanding}",
            }

        # Determine conversion rate by seniority
        rate = JT_CONVERSION_RATES["0_to_3_months"]  # Default
        if contribution_date and self.state.launch_date:
            try:
                contrib = datetime.fromisoformat(contribution_date)
                launch = datetime.fromisoformat(self.state.launch_date)
                months_before = (launch - contrib).days / 30
                if months_before >= 6:
                    rate = JT_CONVERSION_RATES["6_months_plus"]
                elif months_before >= 3:
                    rate = JT_CONVERSION_RATES["3_to_6_months"]
            except (ValueError, TypeError):
                pass

        ur_amount = (jt_amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Update state
        self.state.jt_outstanding -= jt_amount
        self.state.jt_total_converted += jt_amount
        self.state.ur_total_supply += ur_amount
        self.state.ur_circulating += ur_amount

        logger.info(
            f"JT→UR Conversion: {contributor_id} {jt_amount} JT × {rate} = {ur_amount} UR"
        )

        return {
            "success": True,
            "contributor_id": contributor_id,
            "jt_converted": str(jt_amount),
            "conversion_rate": str(rate),
            "ur_received": str(ur_amount),
            "seniority_bonus": str(rate - Decimal("1")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ─── ATOM BONDING CURVE ──────────────────────────────────────────────────

    def buy_atom(self, amount_tokens: Decimal) -> Dict[str, Any]:
        """Buy ATOM tokens via bonding curve."""
        try:
            quote = self.bonding_curve.execute_buy(amount_tokens)
            self.state.atom_supply = self.bonding_curve.current_supply
            self.state.atom_price = self.bonding_curve.current_price()
            self.state.atom_reserve = self.bonding_curve.reserve_balance
            self.state.atom_market_cap = self.state.atom_supply * self.state.atom_price
            return {"success": True, "quote": quote.to_dict()}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def sell_atom(self, amount_tokens: Decimal) -> Dict[str, Any]:
        """Sell ATOM tokens via bonding curve."""
        try:
            quote = self.bonding_curve.execute_sell(amount_tokens)
            self.state.atom_supply = self.bonding_curve.current_supply
            self.state.atom_price = self.bonding_curve.current_price()
            self.state.atom_reserve = self.bonding_curve.reserve_balance
            self.state.atom_market_cap = self.state.atom_supply * self.state.atom_price
            return {"success": True, "quote": quote.to_dict()}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_atom_quote(self, action: str, amount: Decimal) -> Dict[str, Any]:
        """Get a quote without executing."""
        try:
            if action == "buy":
                return {"success": True, "quote": self.bonding_curve.quote_buy(amount).to_dict()}
            elif action == "sell":
                return {"success": True, "quote": self.bonding_curve.quote_sell(amount).to_dict()}
            else:
                return {"success": False, "error": "Action must be 'buy' or 'sell'"}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    # ─── FLOW KEEPER ─────────────────────────────────────────────────────────

    def process_flow(
        self,
        contributor_id: str,
        amount_usd: Decimal,
        flow_type: FlowType,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a Flow Keeper contribution.
        100% goes to community stimulation (NOT infrastructure).

        Args:
            contributor_id: Who is contributing
            amount_usd: Amount in USD
            flow_type: Which flow to direct to
            message: Optional personal message

        Returns:
            Dict with flow token details
        """
        if amount_usd < Decimal("1"):
            return {"success": False, "error": "Minimum flow contribution is $1"}

        token_id = (
            f"FLOW-{flow_type.value.upper()}-"
            f"{datetime.now(timezone.utc).strftime('%Y-%m%d-%H%M%S')}-"
            f"{self._next_flow_token_id:05d}"
        )
        self._next_flow_token_id += 1

        # All Flow Keeper goes to community stimulation
        self.state.flow_total += amount_usd
        self.state.flow_by_type[flow_type.value] = (
            self.state.flow_by_type.get(flow_type.value, Decimal("0")) + amount_usd
        )
        self.state.flow_token_count += 1

        flow_record = {
            "token_id": token_id,
            "contributor_id": contributor_id,
            "amount_usd": str(amount_usd),
            "flow_type": flow_type.value,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sequential_number": self.state.flow_token_count,
        }
        self._flow_history.append(flow_record)

        logger.info(
            f"Flow Keeper: {contributor_id} ${amount_usd} → {flow_type.value} "
            f"(Token: {token_id})"
        )

        return {
            "success": True,
            "token_id": token_id,
            "contributor_id": contributor_id,
            "amount_usd": str(amount_usd),
            "flow_type": flow_type.value,
            "message": message,
            "sequential_number": self.state.flow_token_count,
            "timestamp": flow_record["timestamp"],
        }

    # ─── UR OPERATIONS ────────────────────────────────────────────────────────

    def mint_ur(self, amount: Decimal, reason: str) -> Dict[str, Any]:
        """Mint new UR tokens (controlled emission)."""
        self.state.ur_total_supply += amount
        self.state.ur_treasury += amount
        logger.info(f"UR Minted: {amount} for '{reason}'")
        return {
            "success": True,
            "amount": str(amount),
            "reason": reason,
            "new_total_supply": str(self.state.ur_total_supply),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def burn_ur(self, amount: Decimal, reason: str) -> Dict[str, Any]:
        """Burn UR tokens (deflationary mechanism)."""
        if amount > self.state.ur_treasury:
            return {"success": False, "error": "Insufficient treasury balance"}

        self.state.ur_total_supply -= amount
        self.state.ur_treasury -= amount
        logger.info(f"UR Burned: {amount} for '{reason}'")
        return {
            "success": True,
            "amount": str(amount),
            "reason": reason,
            "new_total_supply": str(self.state.ur_total_supply),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ─── STATE & ANALYTICS ────────────────────────────────────────────────────

    def get_economy_state(self) -> Dict[str, Any]:
        """Get complete economy state for dashboard."""
        return {
            **self.state.to_dict(),
            "bonding_curve": self.bonding_curve.get_state(),
            "nft_availability": self._get_nft_availability(),
            "momentum_progress": self._get_momentum_progress(),
        }

    def _get_nft_availability(self) -> Dict[str, Any]:
        """Get NFT availability per tier."""
        result = {}
        for tier, config in NFT_CONFIG.items():
            minted = self.state.nft_minted.get(tier.value, 0)
            max_supply = config["max_supply"]
            result[tier.value] = {
                "name": config["name"],
                "symbol": config["symbol"],
                "minted": minted,
                "max_supply": max_supply,
                "available": (max_supply - minted) if max_supply else "unlimited",
                "sold_out": max_supply is not None and minted >= max_supply,
                "min_contribution": str(config["min_contribution"]),
            }
        return result

    def _get_momentum_progress(self) -> Dict[str, Any]:
        """Get progress toward Phase I goal."""
        goal = Decimal("100000")  # $100,000 Phase I goal
        raised = self.state.total_raised_usd
        pct = (raised / goal * 100).quantize(Decimal("0.1")) if goal > 0 else Decimal("0")
        return {
            "goal_usd": str(goal),
            "raised_usd": str(raised),
            "percentage": str(min(pct, Decimal("100"))),
            "contributors": self.state.total_contributors,
            "flow_total": str(self.state.flow_total),
        }

    def get_contribution_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent contribution history."""
        return self._contribution_history[-limit:]

    def get_flow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent Flow Keeper history (for the Flow Wall)."""
        return self._flow_history[-limit:]

    def get_price_chart_data(self, points: int = 50) -> List[Dict[str, str]]:
        """Generate bonding curve price chart data."""
        max_supply = self.bonding_curve.max_supply
        step = max_supply / Decimal(str(points))
        data = []
        for i in range(points + 1):
            supply = step * Decimal(str(i))
            price = self.bonding_curve.price_at_supply(supply)
            data.append({
                "supply": str(supply.quantize(Decimal("1"))),
                "price": str(price),
            })
        return data


# =============================================================================
# SINGLETON
# =============================================================================

_tokenomics_service: Optional[TokenomicsService] = None


def get_tokenomics_service() -> TokenomicsService:
    """Get the singleton TokenomicsService instance."""
    global _tokenomics_service
    if _tokenomics_service is None:
        _tokenomics_service = TokenomicsService()
    return _tokenomics_service
