"""
AT·OM — Tokenomics Database Bridge
====================================

Connects TokenomicsService to Supabase for persistent storage.
Maps in-memory operations to real database tables.

Tables used (from 20260205_token_economy.sql):
- token_contributions  → JT minting records
- nft_registry         → NFT ownership
- flow_keeper_ledger   → Flow Keeper contributions
- atom_transactions    → ATOM bonding curve trades
- ur_ledger            → UR mint/burn/transfer
- token_economy_snapshots → Economy state snapshots

Author: AT·OM Collective
"""

from __future__ import annotations

import os
import logging
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Dict, Any, List
from uuid import uuid4

logger = logging.getLogger("nova999.tokenomics_db")


class TokenomicsDB:
    """
    Database bridge for the tokenomics engine.

    Uses Supabase REST API via supabase-py client.
    Falls back to in-memory if Supabase is not configured.
    """

    def __init__(self):
        self._client = None
        self._configured = False
        self._init_client()

    def _init_client(self):
        """Initialize Supabase client from environment."""
        try:
            from supabase import create_client

            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

            if url and key:
                self._client = create_client(url, key)
                self._configured = True
                logger.info(f"TokenomicsDB: Connected to Supabase ({url[:30]}...)")
            else:
                logger.warning("TokenomicsDB: Supabase not configured, using in-memory")
        except ImportError:
            logger.warning("TokenomicsDB: supabase-py not installed, using in-memory")
        except Exception as e:
            logger.error(f"TokenomicsDB: Connection error: {e}")

    @property
    def is_connected(self) -> bool:
        return self._configured and self._client is not None

    # ═══════════════════════════════════════════════════════════════════════════
    # TOKEN CONTRIBUTIONS (JT Minting)
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_contribution(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Save a contribution to token_contributions table."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "contributor_id": data.get("contributor_id"),
                "amount_usd": float(data.get("amount_usd", 0)),
                "jt_tier": data.get("jt_tier"),
                "jt_minted": float(data.get("jt_minted", 0)),
                "jt_bonus_pct": float(data.get("jt_bonus_pct", 0)),
                "nft_tier": data.get("nft_tier"),
                "nft_serial": data.get("nft_serial"),
                "flow_token_id": data.get("flow_token_id"),
                "flow_type": data.get("flow_type"),
                "fund_development": float(data.get("fund_development", 0)),
                "fund_stimulation": float(data.get("fund_stimulation", 0)),
                "fund_structure": float(data.get("fund_structure", 0)),
                "fund_emergency": float(data.get("fund_emergency", 0)),
                "message": data.get("message"),
                "status": "confirmed",
            }

            result = self._client.table("token_contributions").insert(record).execute()
            logger.info(f"TokenomicsDB: Saved contribution {record['id']}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving contribution: {e}")
            return None

    async def get_contributions(self, limit: int = 20) -> List[Dict]:
        """Get recent contributions."""
        if not self.is_connected:
            return []

        try:
            result = (
                self._client.table("token_contributions")
                .select("*")
                .eq("status", "confirmed")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error(f"TokenomicsDB: Error fetching contributions: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════════════════
    # NFT REGISTRY
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_nft(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Save an NFT to nft_registry table."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "tier": data.get("tier"),
                "serial_number": data.get("serial_number"),
                "edition_label": data.get("edition_label"),
                "owner_id": data.get("owner_id"),
                "owner_name": data.get("owner_name"),
                "name": data.get("name"),
                "frequency_hz": data.get("frequency_hz"),
                "contribution_usd": float(data.get("contribution_usd", 0)),
                "contribution_id": data.get("contribution_id"),
                "status": "active",
            }

            result = self._client.table("nft_registry").insert(record).execute()
            logger.info(f"TokenomicsDB: Saved NFT {record['tier']} #{record['serial_number']}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving NFT: {e}")
            return None

    async def get_nft_counts(self) -> Dict[str, int]:
        """Get minted counts per tier."""
        if not self.is_connected:
            return {}

        try:
            result = (
                self._client.table("nft_registry")
                .select("tier")
                .eq("status", "active")
                .execute()
            )
            counts = {}
            for row in (result.data or []):
                tier = row["tier"]
                counts[tier] = counts.get(tier, 0) + 1
            return counts
        except Exception as e:
            logger.error(f"TokenomicsDB: Error fetching NFT counts: {e}")
            return {}

    # ═══════════════════════════════════════════════════════════════════════════
    # FLOW KEEPER LEDGER
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_flow(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Save a Flow Keeper contribution."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "token_id": data.get("token_id"),
                "sequential_number": data.get("sequential_number", 1),
                "contributor_id": data.get("contributor_id"),
                "contributor_name": data.get("contributor_name"),
                "anonymous": data.get("anonymous", False),
                "amount_usd": float(data.get("amount_usd", 0)),
                "flow_type": data.get("flow_type"),
                "message": data.get("message"),
            }

            result = self._client.table("flow_keeper_ledger").insert(record).execute()
            logger.info(f"TokenomicsDB: Saved flow {record['token_id']}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving flow: {e}")
            return None

    async def get_flow_wall(self, limit: int = 50) -> List[Dict]:
        """Get recent flow contributions for the live wall."""
        if not self.is_connected:
            return []

        try:
            result = (
                self._client.table("flow_keeper_ledger")
                .select("*")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data or []
        except Exception as e:
            logger.error(f"TokenomicsDB: Error fetching flow wall: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════════════════
    # ATOM TRANSACTIONS
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_atom_transaction(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Save an ATOM bonding curve transaction."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "action": data.get("action"),
                "account_id": data.get("account_id"),
                "amount_tokens": float(data.get("amount_tokens", 0)),
                "price_per_token": float(data.get("price_per_token", 0)),
                "total_usd": float(data.get("total_usd", 0)),
                "reserve_change": float(data.get("reserve_change", 0)),
                "new_supply": float(data.get("new_supply", 0)),
                "new_price": float(data.get("new_price", 0)),
                "new_reserve": float(data.get("new_reserve", 0)),
            }

            result = self._client.table("atom_transactions").insert(record).execute()
            logger.info(f"TokenomicsDB: Saved ATOM tx {record['action']}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving ATOM tx: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # UR LEDGER
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_ur_transaction(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Save a UR mint/burn/transfer to ur_ledger."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "action": data.get("action"),  # mint, burn, transfer, conversion
                "from_account": data.get("from_account"),
                "to_account": data.get("to_account"),
                "amount": float(data.get("amount", 0)),
                "reason": data.get("reason"),
                "reference_type": data.get("reference_type"),
                "reference_id": data.get("reference_id"),
            }

            result = self._client.table("ur_ledger").insert(record).execute()
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving UR tx: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # ECONOMY SNAPSHOTS
    # ═══════════════════════════════════════════════════════════════════════════

    async def save_snapshot(self, state: Dict[str, Any]) -> Optional[Dict]:
        """Save a complete economy state snapshot."""
        if not self.is_connected:
            return None

        try:
            record = {
                "id": str(uuid4()),
                "ur_total_supply": float(state.get("ur_total_supply", 0)),
                "ur_circulating": float(state.get("ur_circulating", 0)),
                "ur_treasury": float(state.get("ur_treasury", 0)),
                "jt_total_minted": float(state.get("jt_total_minted", 0)),
                "jt_outstanding": float(state.get("jt_outstanding", 0)),
                "jt_converted": float(state.get("jt_total_converted", 0)),
                "atom_supply": float(state.get("atom_supply", 0)),
                "atom_price": float(state.get("atom_price", 0.01)),
                "atom_reserve": float(state.get("atom_reserve", 0)),
                "atom_market_cap": float(state.get("atom_market_cap", 0)),
                "fund_development": float(state.get("fund_balances", {}).get("development", 0)),
                "fund_stimulation": float(state.get("fund_balances", {}).get("stimulation", 0)),
                "fund_structure": float(state.get("fund_balances", {}).get("structure", 0)),
                "fund_emergency": float(state.get("fund_balances", {}).get("emergency", 0)),
                "flow_total": float(state.get("flow_total", 0)),
                "flow_token_count": state.get("flow_token_count", 0),
                "total_raised_usd": float(state.get("total_raised_usd", 0)),
                "total_contributors": state.get("total_contributors", 0),
            }

            # Add NFT counts
            nft_minted = state.get("nft_minted", {})
            record["nft_graine_minted"] = nft_minted.get("graine", 0)
            record["nft_pousse_minted"] = nft_minted.get("pousse", 0)
            record["nft_branche_minted"] = nft_minted.get("branche", 0)
            record["nft_racine_minted"] = nft_minted.get("racine", 0)
            record["nft_arbre_minted"] = nft_minted.get("arbre", 0)

            result = self._client.table("token_economy_snapshots").insert(record).execute()
            logger.info("TokenomicsDB: Economy snapshot saved")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error saving snapshot: {e}")
            return None

    async def get_latest_snapshot(self) -> Optional[Dict]:
        """Get the most recent economy snapshot to restore state."""
        if not self.is_connected:
            return None

        try:
            result = (
                self._client.table("token_economy_snapshots")
                .select("*")
                .order("snapshot_at", desc=True)
                .limit(1)
                .execute()
            )
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"TokenomicsDB: Error fetching snapshot: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # MOMENTUM (Aggregation queries)
    # ═══════════════════════════════════════════════════════════════════════════

    async def get_momentum(self) -> Dict[str, Any]:
        """Get momentum progress from contributions table."""
        if not self.is_connected:
            return {
                "total_contributions": 0,
                "unique_contributors": 0,
                "total_raised": 0,
                "total_jt_minted": 0,
            }

        try:
            result = (
                self._client.table("token_contributions")
                .select("amount_usd, jt_minted, contributor_id")
                .in_("status", ["confirmed", "converted"])
                .execute()
            )

            rows = result.data or []
            contributors = set()
            total_raised = 0
            total_jt = 0

            for row in rows:
                total_raised += float(row.get("amount_usd", 0))
                total_jt += float(row.get("jt_minted", 0))
                contributors.add(row.get("contributor_id"))

            return {
                "total_contributions": len(rows),
                "unique_contributors": len(contributors),
                "total_raised": total_raised,
                "total_jt_minted": total_jt,
            }

        except Exception as e:
            logger.error(f"TokenomicsDB: Error fetching momentum: {e}")
            return {
                "total_contributions": 0,
                "unique_contributors": 0,
                "total_raised": 0,
                "total_jt_minted": 0,
            }


# ═══════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_db_instance: Optional[TokenomicsDB] = None


def get_tokenomics_db() -> TokenomicsDB:
    """Get the singleton TokenomicsDB instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = TokenomicsDB()
    return _db_instance
