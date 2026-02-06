"""
AT·OM — Tokenomics ↔ Hedera Bridge
====================================

Connects the TokenomicsService to Hedera HTS for real on-chain operations.
Records all transactions on Hedera Consensus Service (HCS) as immutable audit logs.

Token IDs (AT-OM$ — Testnet):
- ATOM Token:    0.0.7780104  ($ATOM, fungible)
- NFT Collection: 0.0.7780274 (AT-OM : Back to Light)
- Operator:      0.0.7774579

Author: AT·OM Collective
"""

from __future__ import annotations

import os
import json
import logging
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Dict, Any

logger = logging.getLogger("nova999.tokenomics_hedera")

# AT-OM$ Token Configuration
ATOM_TOKEN_ID = os.environ.get("HEDERA_TOKEN_ID", "0.0.7780104")
NFT_COLLECTION_ID = os.environ.get("NFT_COLLECTION_ID", "0.0.7780274")
HCS_TOPIC_ID = os.environ.get("HEDERA_HCS_TOPIC_ID", "")
SIMULATION_MODE = os.environ.get("HEDERA_SIMULATION_MODE", "true").lower() == "true"


class TokenomicsHederaBridge:
    """
    Bridge between TokenomicsService and Hedera on-chain operations.

    Operations:
    - mint_jt_on_chain: Record JT minting on HCS (audit)
    - mint_nft_on_chain: Mint NFT on HTS (real NFT)
    - record_flow_on_chain: Record Flow Keeper on HCS (audit)
    - record_atom_trade_on_chain: Record ATOM trade on HCS (audit)
    - mint_ur_on_chain: Mint UR tokens on HTS
    """

    def __init__(self):
        self._hedera_service = None
        self._simulation = SIMULATION_MODE
        self._tx_log = []

        if not self._simulation:
            self._init_hedera()

    def _init_hedera(self):
        """Initialize the Hedera service."""
        try:
            try:
                from app.services.hedera_service import HederaService
            except ImportError:
                from backend.app.services.hedera_service import HederaService
            self._hedera_service = HederaService()
            logger.info(f"Hedera Bridge: Connected (Token: {ATOM_TOKEN_ID}, NFT: {NFT_COLLECTION_ID})")
        except ImportError:
            logger.warning("Hedera Bridge: hedera_service not available, using simulation")
            self._simulation = True
        except Exception as e:
            logger.error(f"Hedera Bridge: Init error: {e}")
            self._simulation = True

    @property
    def is_live(self) -> bool:
        """Check if we're connected to real Hedera network."""
        return not self._simulation and self._hedera_service is not None

    # ═══════════════════════════════════════════════════════════════════════════
    # NFT MINTING (Real HTS)
    # ═══════════════════════════════════════════════════════════════════════════

    async def mint_nft(
        self,
        tier: str,
        serial_number: int,
        owner_id: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Mint a real NFT on Hedera for an investor.

        Args:
            tier: NFT tier (graine, pousse, branche, racine, arbre)
            serial_number: Sequential number within tier
            owner_id: UUID of the owner
            metadata: NFT metadata dict

        Returns:
            Dict with hedera_tx_id, hedera_serial, etc.
        """
        if self._simulation:
            tx_id = f"SIM-NFT-{tier}-{serial_number}-{datetime.now(timezone.utc).strftime('%H%M%S')}"
            logger.info(f"[SIMULATION] NFT Mint: {tier} #{serial_number} → {tx_id}")
            result = {
                "success": True,
                "simulated": True,
                "hedera_tx_id": tx_id,
                "hedera_token_id": NFT_COLLECTION_ID,
                "hedera_serial": serial_number,
                "tier": tier,
            }
            self._tx_log.append(result)
            return result

        # Real Hedera mint
        try:
            # Serialize metadata to bytes (max 100 bytes for HTS NFT metadata)
            meta_compact = json.dumps({
                "t": tier[:2],
                "s": serial_number,
                "o": owner_id[:8],
            })
            metadata_bytes = meta_compact.encode("utf-8")[:100]

            result = await self._hedera_service.mint_nft(
                token_id=NFT_COLLECTION_ID,
                metadata=metadata_bytes,
            )

            logger.info(f"NFT Minted on Hedera: {tier} #{serial_number} → {result.transaction_id}")

            return {
                "success": result.success,
                "simulated": False,
                "hedera_tx_id": result.transaction_id,
                "hedera_token_id": NFT_COLLECTION_ID,
                "hedera_serial": serial_number,
                "tier": tier,
            }

        except Exception as e:
            logger.error(f"NFT Mint error: {e}")
            return {"success": False, "error": str(e)}

    # ═══════════════════════════════════════════════════════════════════════════
    # HCS AUDIT LOG (Immutable records)
    # ═══════════════════════════════════════════════════════════════════════════

    async def log_to_hcs(self, event_type: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Log an event to Hedera Consensus Service (immutable audit trail).

        Args:
            event_type: Type of event (contribution, nft_mint, flow, atom_trade, ur_mint, ur_burn)
            data: Event data to log

        Returns:
            HCS sequence number or None
        """
        message = {
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {k: str(v) if isinstance(v, Decimal) else v for k, v in data.items()},
        }

        if self._simulation:
            seq = len(self._tx_log) + 1
            logger.info(f"[SIMULATION] HCS Log: {event_type} → seq#{seq}")
            self._tx_log.append({"hcs": True, "seq": seq, **message})
            return str(seq)

        if not HCS_TOPIC_ID:
            logger.warning("HCS Topic ID not configured, skipping audit log")
            return None

        try:
            result = await self._hedera_service.submit_hcs_message(
                topic_id=HCS_TOPIC_ID,
                message=json.dumps(message),
            )
            logger.info(f"HCS Logged: {event_type} → {result.transaction_id}")
            return result.transaction_id

        except Exception as e:
            logger.error(f"HCS Log error: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # CONVENIENCE METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    async def log_contribution(self, contribution_data: Dict) -> Optional[str]:
        """Log a JT contribution to HCS."""
        return await self.log_to_hcs("contribution", contribution_data)

    async def log_flow(self, flow_data: Dict) -> Optional[str]:
        """Log a Flow Keeper contribution to HCS."""
        return await self.log_to_hcs("flow_keeper", flow_data)

    async def log_atom_trade(self, trade_data: Dict) -> Optional[str]:
        """Log an ATOM buy/sell to HCS."""
        return await self.log_to_hcs("atom_trade", trade_data)

    async def log_ur_operation(self, operation_data: Dict) -> Optional[str]:
        """Log a UR mint/burn to HCS."""
        return await self.log_to_hcs("ur_operation", operation_data)

    def get_transaction_log(self) -> list:
        """Get simulation transaction log."""
        return self._tx_log


# ═══════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_bridge_instance: Optional[TokenomicsHederaBridge] = None


def get_hedera_bridge() -> TokenomicsHederaBridge:
    """Get the singleton Hedera bridge instance."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = TokenomicsHederaBridge()
    return _bridge_instance
