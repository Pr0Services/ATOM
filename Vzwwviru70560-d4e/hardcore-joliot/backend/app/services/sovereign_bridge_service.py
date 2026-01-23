"""
Sovereign Bridge Service - Central Integration Hub for AT·OM/CHE·NU

This service connects all sovereign systems:
- Hedera (UR tokens, HCS audit)
- Exfiltration Engine (fiat extraction)
- The Forge (project management)
- Sovereignty RBAC (access control)
- Nova Agent (AI liaison)
- Sentinel Protocol (peace consensus)

It provides unified operations that span multiple systems while
maintaining sovereignty principles and immutable audit trails.

Author: AT·OM Collective
Version: 1.0.0
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from app.services.hedera_service import (
    get_hedera_service,
    HederaService,
    TransactionResult
)

logger = logging.getLogger(__name__)


# ==================== ENUMS & CONSTANTS ====================

class SystemModule(Enum):
    """Available sovereign system modules"""
    HEDERA = "hedera"
    EXFILTRATION = "exfiltration"
    FORGE = "forge"
    SOVEREIGNTY = "sovereignty"
    NOVA = "nova"
    SENTINEL = "sentinel"
    PROGRESSIVE_UNLOCK = "progressive_unlock"


class EventType(Enum):
    """Types of cross-system events"""
    # Economic events
    TOKEN_MINT = "token_mint"
    TOKEN_BURN = "token_burn"
    TOKEN_TRANSFER = "token_transfer"
    CONVERSION_REQUEST = "conversion_request"
    CONVERSION_COMPLETE = "conversion_complete"

    # Exfiltration events
    EXFILTRATION_START = "exfiltration_start"
    EXFILTRATION_COMPLETE = "exfiltration_complete"
    ASSET_ACQUISITION = "asset_acquisition"
    RISK_ALERT = "risk_alert"
    EMERGENCY_MODE = "emergency_mode"

    # Forge events
    PROJECT_CREATED = "project_created"
    ROLE_ASSIGNED = "role_assigned"
    DISBURSEMENT_SENT = "disbursement_sent"
    MILESTONE_COMPLETE = "milestone_complete"

    # Sovereignty events
    SOVEREIGNTY_PROMOTED = "sovereignty_promoted"
    INVITATION_SENT = "invitation_sent"
    SACRED_KNOWLEDGE_ACCESS = "sacred_knowledge_access"

    # Nova events
    NOVA_INTERACTION = "nova_interaction"
    LAYOUT_CHANGED = "layout_changed"
    PREFERENCE_UPDATED = "preference_updated"

    # Sentinel events
    THREAT_DETECTED = "threat_detected"
    CONSENSUS_REQUESTED = "consensus_requested"
    VOTE_CAST = "vote_cast"
    RESPONSE_EXECUTED = "response_executed"

    # Module events
    MODULE_UNLOCKED = "module_unlocked"
    MODULE_DISMISSED = "module_dismissed"


@dataclass
class SovereignEvent:
    """Represents a cross-system event"""
    event_type: EventType
    module: SystemModule
    user_id: str
    timestamp: datetime
    data: Dict[str, Any]
    hedera_tx_id: Optional[str] = None
    hcs_sequence: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type.value,
            'module': self.module.value,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'hedera_tx_id': self.hedera_tx_id,
            'hcs_sequence': self.hcs_sequence
        }


# ==================== BRIDGE SERVICE ====================

class SovereignBridgeService:
    """
    Central orchestration service for AT·OM sovereign systems.

    Coordinates operations across:
    - Hedera blockchain (UR tokens, immutable logs)
    - PostgreSQL database (state, history)
    - Real-time events (WebSocket)
    - AI agents (Nova, L4)
    """

    def __init__(self, db_pool=None):
        """Initialize bridge service"""
        self.hedera = get_hedera_service()
        self.db_pool = db_pool
        self._event_handlers: Dict[EventType, List[callable]] = {}
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize all connected services"""
        if self._initialized:
            return True

        # Initialize Hedera connection
        hedera_ok = await self.hedera.initialize()
        if not hedera_ok:
            logger.warning("Hedera initialization failed, running in limited mode")

        self._initialized = True
        return True

    # ==================== EVENT SYSTEM ====================

    def register_handler(self, event_type: EventType, handler: callable):
        """Register a handler for an event type"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    async def emit_event(self, event: SovereignEvent) -> bool:
        """
        Emit an event across the sovereign system.

        1. Log to HCS for immutable record
        2. Store in database
        3. Notify registered handlers
        4. Broadcast via WebSocket
        """
        try:
            # Log to HCS
            if self.hedera.is_initialized():
                await self.hedera._log_to_hcs(event.to_dict())

            # Store in database
            if self.db_pool:
                await self._store_event(event)

            # Notify handlers
            handlers = self._event_handlers.get(event.event_type, [])
            for handler in handlers:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")

            return True

        except Exception as e:
            logger.error(f"Failed to emit event: {e}")
            return False

    async def _store_event(self, event: SovereignEvent):
        """Store event in database"""
        if not self.db_pool:
            return

        # Implementation would insert into sovereign_events table
        pass

    # ==================== ECONOMIC OPERATIONS ====================

    async def process_subscription(
        self,
        user_id: str,
        tier: str,
        amount_cad: Decimal,
        stripe_payment_id: str
    ) -> Dict[str, Any]:
        """
        Process a new subscription payment.

        Flow:
        1. Record fiat payment in exfiltration reserves
        2. Calculate UR amount based on current rate
        3. Mint UR tokens to user's Hedera account
        4. Update user's subscription status
        5. Log event to HCS
        """
        result = {
            'success': False,
            'ur_minted': Decimal('0'),
            'hedera_tx_id': None,
            'error': None
        }

        try:
            # Get user's Hedera account
            user_account = await self._get_user_hedera_account(user_id)

            # Calculate UR amount (1 CAD = ~0.74 UR at base rate)
            ur_rate = await self._get_current_ur_rate('CAD')
            ur_amount = amount_cad / ur_rate

            # Mint UR tokens
            mint_result = await self.hedera.mint_ur(
                amount=ur_amount,
                reason=f"Subscription: {tier}",
                recipient_account=user_account
            )

            if mint_result.success:
                result['success'] = True
                result['ur_minted'] = ur_amount
                result['hedera_tx_id'] = mint_result.transaction_id

                # Emit event
                await self.emit_event(SovereignEvent(
                    event_type=EventType.TOKEN_MINT,
                    module=SystemModule.HEDERA,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                    data={
                        'amount_cad': str(amount_cad),
                        'ur_minted': str(ur_amount),
                        'tier': tier,
                        'stripe_payment_id': stripe_payment_id
                    },
                    hedera_tx_id=mint_result.transaction_id
                ))
            else:
                result['error'] = mint_result.error

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Subscription processing error: {e}")

        return result

    async def process_disbursement(
        self,
        project_id: str,
        recipient_id: str,
        amount_ur: Decimal,
        description: str,
        approver_id: str
    ) -> Dict[str, Any]:
        """
        Process a project disbursement from The Forge.

        Flow:
        1. Verify project budget has sufficient funds
        2. Transfer UR from project treasury to recipient
        3. Update project budget tracking
        4. Log disbursement event
        """
        result = {
            'success': False,
            'transaction_id': None,
            'error': None
        }

        try:
            # Get accounts
            project_account = await self._get_project_hedera_account(project_id)
            recipient_account = await self._get_user_hedera_account(recipient_id)

            # Execute transfer
            transfer_result = await self.hedera.transfer_ur(
                from_account=project_account,
                to_account=recipient_account,
                amount=amount_ur,
                memo=f"Forge disbursement: {description[:50]}"
            )

            if transfer_result.success:
                result['success'] = True
                result['transaction_id'] = transfer_result.transaction_id

                # Emit event
                await self.emit_event(SovereignEvent(
                    event_type=EventType.DISBURSEMENT_SENT,
                    module=SystemModule.FORGE,
                    user_id=approver_id,
                    timestamp=datetime.utcnow(),
                    data={
                        'project_id': project_id,
                        'recipient_id': recipient_id,
                        'amount_ur': str(amount_ur),
                        'description': description
                    },
                    hedera_tx_id=transfer_result.transaction_id
                ))
            else:
                result['error'] = transfer_result.error

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Disbursement error: {e}")

        return result

    async def execute_exfiltration(
        self,
        extraction_percentage: int,
        reason: str,
        executor_id: str
    ) -> Dict[str, Any]:
        """
        Execute exfiltration from fiat reserves to sovereign assets.

        Flow:
        1. Calculate extraction amount based on percentage
        2. Initiate fiat withdrawal
        3. Acquire tangible assets or mint UR
        4. Update exfiltration tracking
        5. Log to HCS for transparency
        """
        result = {
            'success': False,
            'extracted_cad': Decimal('0'),
            'ur_minted': Decimal('0'),
            'assets_acquired': [],
            'error': None
        }

        try:
            # Get current fiat reserves
            reserves = await self._get_fiat_reserves()
            extraction_amount = reserves['cad'] * Decimal(extraction_percentage) / 100

            if extraction_amount < Decimal('100'):
                result['error'] = "Extraction amount too small"
                return result

            # Calculate UR mint (70% of extraction goes to UR)
            ur_rate = await self._get_current_ur_rate('CAD')
            ur_to_mint = (extraction_amount * Decimal('0.7')) / ur_rate

            # Mint UR to treasury
            mint_result = await self.hedera.mint_ur(
                amount=ur_to_mint,
                reason=f"Exfiltration: {reason}"
            )

            if mint_result.success:
                result['success'] = True
                result['extracted_cad'] = extraction_amount
                result['ur_minted'] = ur_to_mint

                # Emit event
                await self.emit_event(SovereignEvent(
                    event_type=EventType.EXFILTRATION_COMPLETE,
                    module=SystemModule.EXFILTRATION,
                    user_id=executor_id,
                    timestamp=datetime.utcnow(),
                    data={
                        'extraction_percentage': extraction_percentage,
                        'extracted_cad': str(extraction_amount),
                        'ur_minted': str(ur_to_mint),
                        'reason': reason
                    },
                    hedera_tx_id=mint_result.transaction_id
                ))
            else:
                result['error'] = mint_result.error

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Exfiltration error: {e}")

        return result

    # ==================== SOVEREIGNTY OPERATIONS ====================

    async def promote_sovereignty(
        self,
        user_id: str,
        new_level: int,
        promoter_id: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Promote a user's sovereignty level.

        Includes special handling for:
        - Founder promotion (level 5+): Sacred knowledge access
        - Guardian promotion (level 6): Governance voting rights
        - Sovereign promotion (level 7): Full system access
        """
        result = {
            'success': False,
            'previous_level': None,
            'new_level': new_level,
            'permissions_granted': [],
            'error': None
        }

        try:
            # Get current level
            current_level = await self._get_user_sovereignty_level(user_id)
            result['previous_level'] = current_level

            # Validate promotion
            promoter_level = await self._get_user_sovereignty_level(promoter_id)
            if promoter_level < new_level:
                result['error'] = "Promoter cannot grant higher level than their own"
                return result

            # Update sovereignty in database
            # (Implementation would update sovereignty_assignments table)

            # Determine new permissions
            permissions = self._get_permissions_for_level(new_level)
            result['permissions_granted'] = permissions

            # Emit event
            await self.emit_event(SovereignEvent(
                event_type=EventType.SOVEREIGNTY_PROMOTED,
                module=SystemModule.SOVEREIGNTY,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                data={
                    'previous_level': current_level,
                    'new_level': new_level,
                    'promoter_id': promoter_id,
                    'reason': reason,
                    'permissions': permissions
                }
            ))

            # Log governance action to HCS
            await self.hedera.log_governance_action(
                action_type="SOVEREIGNTY_PROMOTION",
                proposal_id=f"promo_{user_id}_{datetime.utcnow().timestamp()}",
                result="APPROVED",
                metadata={
                    'user_id': user_id,
                    'new_level': new_level,
                    'promoter': promoter_id
                }
            )

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Sovereignty promotion error: {e}")

        return result

    def _get_permissions_for_level(self, level: int) -> List[str]:
        """Get permissions granted at a sovereignty level"""
        permissions = {
            1: ['view_basic'],
            2: ['view_basic', 'create_content'],
            3: ['view_basic', 'create_content', 'view_advanced', 'participate_governance'],
            4: ['view_basic', 'create_content', 'view_advanced', 'participate_governance', 'moderate'],
            5: ['view_basic', 'create_content', 'view_advanced', 'participate_governance', 'moderate', 'sacred_knowledge', 'vibrational_interface'],
            6: ['view_basic', 'create_content', 'view_advanced', 'participate_governance', 'moderate', 'sacred_knowledge', 'vibrational_interface', 'governance_vote', 'guardian_duties'],
            7: ['*']  # All permissions
        }
        return permissions.get(level, permissions[1])

    # ==================== SENTINEL OPERATIONS ====================

    async def process_sentinel_vote(
        self,
        threat_id: str,
        guardian_id: str,
        vote: str,  # 'approve', 'reject', 'abstain', 'veto'
        justification: str
    ) -> Dict[str, Any]:
        """
        Process a peace guardian's vote on a threat response.

        Flow:
        1. Verify guardian status
        2. Record vote
        3. Check if consensus reached
        4. If consensus, execute response
        5. Log to HCS for transparency
        """
        result = {
            'success': False,
            'consensus_reached': False,
            'response_executed': False,
            'error': None
        }

        try:
            # Verify guardian status
            sovereignty_level = await self._get_user_sovereignty_level(guardian_id)
            if sovereignty_level < 6:
                result['error'] = "Only guardians (level 6+) can vote on threats"
                return result

            # Record vote (implementation would update guardian_votes table)

            # Emit event
            await self.emit_event(SovereignEvent(
                event_type=EventType.VOTE_CAST,
                module=SystemModule.SENTINEL,
                user_id=guardian_id,
                timestamp=datetime.utcnow(),
                data={
                    'threat_id': threat_id,
                    'vote': vote,
                    'justification': justification
                }
            ))

            # Log to HCS
            await self.hedera.log_governance_action(
                action_type="SENTINEL_VOTE",
                proposal_id=threat_id,
                voter_id=guardian_id,
                vote=vote,
                metadata={'justification': justification}
            )

            # Check consensus
            consensus = await self._check_sentinel_consensus(threat_id)
            if consensus['reached']:
                result['consensus_reached'] = True

                # Execute response if approved
                if consensus['decision'] == 'approve':
                    exec_result = await self._execute_sentinel_response(threat_id)
                    result['response_executed'] = exec_result

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Sentinel vote error: {e}")

        return result

    async def _check_sentinel_consensus(self, threat_id: str) -> Dict[str, Any]:
        """Check if consensus has been reached on a threat"""
        # Implementation would query guardian_votes and calculate consensus
        return {
            'reached': False,
            'decision': None,
            'approve_count': 0,
            'reject_count': 0,
            'threshold': 0.67
        }

    async def _execute_sentinel_response(self, threat_id: str) -> bool:
        """Execute the approved response to a threat"""
        # Implementation would execute the response plan
        return True

    # ==================== MODULE UNLOCK OPERATIONS ====================

    async def unlock_module(
        self,
        user_id: str,
        module_id: str,
        unlock_method: str  # 'accepted', 'purchased', 'earned'
    ) -> Dict[str, Any]:
        """
        Unlock a module for a user.

        If module requires UR payment, processes the transaction.
        """
        result = {
            'success': False,
            'module_id': module_id,
            'ur_spent': Decimal('0'),
            'tutorial_available': False,
            'error': None
        }

        try:
            # Get module info
            module = await self._get_module_info(module_id)
            if not module:
                result['error'] = "Module not found"
                return result

            # Check if already unlocked
            already_unlocked = await self._is_module_unlocked(user_id, module_id)
            if already_unlocked:
                result['error'] = "Module already unlocked"
                return result

            # Process payment if required
            if module.get('ur_cost', 0) > 0 and unlock_method == 'purchased':
                user_account = await self._get_user_hedera_account(user_id)
                treasury_account = await self._get_treasury_account()

                transfer_result = await self.hedera.transfer_ur(
                    from_account=user_account,
                    to_account=treasury_account,
                    amount=Decimal(str(module['ur_cost'])),
                    memo=f"Module unlock: {module_id}"
                )

                if not transfer_result.success:
                    result['error'] = f"Payment failed: {transfer_result.error}"
                    return result

                result['ur_spent'] = Decimal(str(module['ur_cost']))

            # Unlock module in database
            # (Implementation would insert into user_modules table)

            # Emit event
            await self.emit_event(SovereignEvent(
                event_type=EventType.MODULE_UNLOCKED,
                module=SystemModule.PROGRESSIVE_UNLOCK,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                data={
                    'module_id': module_id,
                    'unlock_method': unlock_method,
                    'ur_spent': str(result['ur_spent'])
                }
            ))

            result['success'] = True
            result['tutorial_available'] = module.get('has_tutorial', False)

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Module unlock error: {e}")

        return result

    # ==================== HELPER METHODS ====================

    async def _get_user_hedera_account(self, user_id: str) -> Optional[str]:
        """Get user's Hedera account ID from database"""
        # Implementation would query member_balances table
        return None

    async def _get_project_hedera_account(self, project_id: str) -> Optional[str]:
        """Get project's Hedera account ID"""
        # Implementation would query forge_projects table
        return None

    async def _get_treasury_account(self) -> str:
        """Get system treasury Hedera account"""
        return os.getenv('HEDERA_TREASURY_ACCOUNT', '')

    async def _get_current_ur_rate(self, currency: str) -> Decimal:
        """Get current UR exchange rate"""
        # Implementation would query liquidity_pool table
        rates = {'CAD': Decimal('1.35'), 'USD': Decimal('1.00')}
        return rates.get(currency, Decimal('1.00'))

    async def _get_fiat_reserves(self) -> Dict[str, Decimal]:
        """Get current fiat reserves"""
        # Implementation would query exfiltration_fund table
        return {'cad': Decimal('0'), 'usd': Decimal('0')}

    async def _get_user_sovereignty_level(self, user_id: str) -> int:
        """Get user's sovereignty level"""
        # Implementation would query sovereignty_assignments table
        return 1

    async def _get_module_info(self, module_id: str) -> Optional[Dict]:
        """Get module information"""
        # Implementation would query unlockable_modules table
        return None

    async def _is_module_unlocked(self, user_id: str, module_id: str) -> bool:
        """Check if user has unlocked a module"""
        # Implementation would query user_modules table
        return False

    # ==================== DASHBOARD AGGREGATION ====================

    async def get_unified_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        Get unified dashboard data across all sovereign systems.

        Aggregates data from:
        - Hedera (UR balance, transactions)
        - Exfiltration (fund status, risk level)
        - Forge (active projects, roles)
        - Sovereignty (level, permissions)
        - Sentinel (threat status)
        - Modules (unlocked features)
        """
        dashboard = {
            'user_id': user_id,
            'generated_at': datetime.utcnow().isoformat(),
            'hedera': {},
            'exfiltration': {},
            'forge': {},
            'sovereignty': {},
            'sentinel': {},
            'modules': {},
            'nova_suggestions': []
        }

        try:
            # Get Hedera data
            user_account = await self._get_user_hedera_account(user_id)
            if user_account:
                success, balance, _ = await self.hedera.get_ur_balance(user_account)
                dashboard['hedera'] = {
                    'account_id': user_account,
                    'ur_balance': str(balance) if success else '0',
                    'connected': True
                }
            else:
                dashboard['hedera'] = {'connected': False}

            # Get sovereignty data
            level = await self._get_user_sovereignty_level(user_id)
            dashboard['sovereignty'] = {
                'level': level,
                'level_name': self._get_level_name(level),
                'permissions': self._get_permissions_for_level(level)
            }

            # Placeholder for other systems
            dashboard['exfiltration'] = {
                'risk_level': 'LOW',
                'extraction_rate': 10
            }

            dashboard['forge'] = {
                'active_projects': 0,
                'pending_disbursements': 0
            }

            dashboard['sentinel'] = {
                'global_threat_level': 'GREEN',
                'pending_votes': 0
            }

            dashboard['modules'] = {
                'unlocked_count': 0,
                'available_count': 0
            }

        except Exception as e:
            logger.error(f"Dashboard aggregation error: {e}")
            dashboard['error'] = str(e)

        return dashboard

    def _get_level_name(self, level: int) -> str:
        """Get sovereignty level name"""
        names = {
            1: 'GUEST',
            2: 'MEMBER',
            3: 'INITIATE',
            4: 'ADEPT',
            5: 'FOUNDER',
            6: 'GUARDIAN',
            7: 'SOVEREIGN'
        }
        return names.get(level, 'UNKNOWN')


# ==================== SINGLETON INSTANCE ====================

_bridge_service: Optional[SovereignBridgeService] = None


def get_bridge_service() -> SovereignBridgeService:
    """Get or create the singleton bridge service instance"""
    global _bridge_service
    if _bridge_service is None:
        _bridge_service = SovereignBridgeService()
    return _bridge_service


async def initialize_bridge() -> bool:
    """Initialize the bridge service"""
    service = get_bridge_service()
    return await service.initialize()
