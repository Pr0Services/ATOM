"""
Hedera Hashgraph Integration Service for AT·OM/CHE·NU Sovereign Economy

This service provides complete integration with Hedera's:
- HTS (Hedera Token Service) for UR token operations
- HCS (Hedera Consensus Service) for immutable audit logs
- Account management for sovereign members

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

# Hedera SDK imports (requires: pip install hedera-sdk-py)
try:
    from hedera import (
        Client,
        AccountId,
        PrivateKey,
        PublicKey,
        Hbar,
        TokenId,
        TokenCreateTransaction,
        TokenMintTransaction,
        TokenBurnTransaction,
        TransferTransaction,
        TokenAssociateTransaction,
        AccountCreateTransaction,
        AccountBalanceQuery,
        TokenInfoQuery,
        TransactionRecordQuery,
        TopicId,
        TopicCreateTransaction,
        TopicMessageSubmitTransaction,
        TopicMessageQuery,
        Status,
        TokenType,
        TokenSupplyType,
    )
    HEDERA_SDK_AVAILABLE = True
except ImportError:
    HEDERA_SDK_AVAILABLE = False
    logging.warning("Hedera SDK not installed. Running in simulation mode.")

logger = logging.getLogger(__name__)


class HederaNetwork(Enum):
    """Hedera network environments"""
    MAINNET = "mainnet"
    TESTNET = "testnet"
    PREVIEWNET = "previewnet"
    LOCAL = "local"


class TransactionType(Enum):
    """Types of Hedera transactions"""
    MINT = "mint"
    BURN = "burn"
    TRANSFER = "transfer"
    ASSOCIATE = "associate"
    CREATE_ACCOUNT = "create_account"
    CONSENSUS_MESSAGE = "consensus_message"
    GOVERNANCE_VOTE = "governance_vote"
    CONVERSION = "conversion"


@dataclass
class HederaConfig:
    """Configuration for Hedera connection"""
    network: HederaNetwork
    operator_id: str
    operator_key: str
    ur_token_id: Optional[str] = None
    hcs_topic_id: Optional[str] = None
    mirror_node_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'HederaConfig':
        """Load configuration from environment variables"""
        network_str = os.getenv('HEDERA_NETWORK', 'testnet')
        return cls(
            network=HederaNetwork(network_str),
            operator_id=os.getenv('HEDERA_OPERATOR_ID', ''),
            operator_key=os.getenv('HEDERA_OPERATOR_KEY', ''),
            ur_token_id=os.getenv('HEDERA_UR_TOKEN_ID'),
            hcs_topic_id=os.getenv('HEDERA_HCS_TOPIC_ID'),
            mirror_node_url=os.getenv('HEDERA_MIRROR_NODE_URL')
        )


@dataclass
class TransactionResult:
    """Result of a Hedera transaction"""
    success: bool
    transaction_id: Optional[str]
    receipt_status: Optional[str]
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result


@dataclass
class URTokenInfo:
    """Information about the UR token"""
    token_id: str
    name: str
    symbol: str
    decimals: int
    total_supply: Decimal
    circulating_supply: Decimal
    treasury_balance: Decimal
    is_paused: bool
    admin_key: Optional[str]
    supply_key: Optional[str]


class HederaService:
    """
    Core Hedera integration service for AT·OM sovereign economy.

    Handles all interactions with Hedera Hashgraph including:
    - UR token minting, burning, and transfers
    - Account creation and management
    - Consensus logging via HCS
    - Governance operations
    """

    def __init__(self, config: Optional[HederaConfig] = None):
        """Initialize Hedera service with configuration"""
        self.config = config or HederaConfig.from_env()
        self.client: Optional[Client] = None
        self._initialized = False
        self._simulation_mode = not HEDERA_SDK_AVAILABLE

        # Simulation state (for testing without real Hedera connection)
        self._sim_balances: Dict[str, Decimal] = {}
        self._sim_total_supply = Decimal('0')
        self._sim_transactions: List[Dict] = []
        self._sim_accounts: Dict[str, Dict] = {}

    async def initialize(self) -> bool:
        """
        Initialize connection to Hedera network.
        Returns True if successful, False otherwise.
        """
        if self._initialized:
            return True

        if self._simulation_mode:
            logger.info("Hedera service running in SIMULATION mode")
            self._initialized = True
            return True

        try:
            # Initialize client based on network
            if self.config.network == HederaNetwork.MAINNET:
                self.client = Client.forMainnet()
            elif self.config.network == HederaNetwork.TESTNET:
                self.client = Client.forTestnet()
            elif self.config.network == HederaNetwork.PREVIEWNET:
                self.client = Client.forPreviewnet()
            else:
                raise ValueError(f"Unsupported network: {self.config.network}")

            # Set operator account
            operator_id = AccountId.fromString(self.config.operator_id)
            operator_key = PrivateKey.fromString(self.config.operator_key)
            self.client.setOperator(operator_id, operator_key)

            # Verify connection by querying operator balance
            balance = await AccountBalanceQuery().setAccountId(operator_id).execute(self.client)
            logger.info(f"Connected to Hedera {self.config.network.value}. Operator balance: {balance.hbars}")

            self._initialized = True
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Hedera client: {e}")
            return False

    async def close(self):
        """Close Hedera client connection"""
        if self.client:
            self.client.close()
            self._initialized = False

    # ==================== TOKEN OPERATIONS ====================

    async def create_ur_token(
        self,
        name: str = "Unité de Résonance",
        symbol: str = "UR",
        decimals: int = 8,
        initial_supply: int = 0,
        max_supply: Optional[int] = None
    ) -> TransactionResult:
        """
        Create the UR token on Hedera Token Service.
        Should only be called once during initial deployment.
        """
        if self._simulation_mode:
            token_id = f"0.0.{1000000 + len(self._sim_transactions)}"
            self._sim_transactions.append({
                'type': 'CREATE_TOKEN',
                'token_id': token_id,
                'name': name,
                'symbol': symbol,
                'timestamp': datetime.utcnow().isoformat()
            })
            return TransactionResult(
                success=True,
                transaction_id=f"sim_tx_{len(self._sim_transactions)}",
                receipt_status="SUCCESS",
                metadata={'token_id': token_id}
            )

        try:
            operator_key = PrivateKey.fromString(self.config.operator_key)

            # Build token creation transaction
            transaction = (
                TokenCreateTransaction()
                .setTokenName(name)
                .setTokenSymbol(symbol)
                .setDecimals(decimals)
                .setInitialSupply(initial_supply)
                .setTokenType(TokenType.FUNGIBLE_COMMON)
                .setSupplyType(TokenSupplyType.INFINITE if max_supply is None else TokenSupplyType.FINITE)
                .setTreasuryAccountId(AccountId.fromString(self.config.operator_id))
                .setAdminKey(operator_key.getPublicKey())
                .setSupplyKey(operator_key.getPublicKey())
                .setFreezeKey(operator_key.getPublicKey())
                .setPauseKey(operator_key.getPublicKey())
            )

            if max_supply:
                transaction.setMaxSupply(max_supply)

            # Execute and get receipt
            response = await transaction.execute(self.client)
            receipt = await response.getReceipt(self.client)

            token_id = str(receipt.tokenId)
            logger.info(f"Created UR token with ID: {token_id}")

            return TransactionResult(
                success=True,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'token_id': token_id}
            )

        except Exception as e:
            logger.error(f"Failed to create UR token: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def mint_ur(
        self,
        amount: Decimal,
        reason: str,
        recipient_account: Optional[str] = None
    ) -> TransactionResult:
        """
        Mint new UR tokens.

        Args:
            amount: Amount of UR to mint (in token units, not smallest denomination)
            reason: Reason for minting (for audit log)
            recipient_account: If provided, transfer directly to this account
        """
        if not self.config.ur_token_id:
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error="UR token not configured"
            )

        # Convert to smallest denomination (8 decimals)
        amount_smallest = int(amount * Decimal('100000000'))

        if self._simulation_mode:
            self._sim_total_supply += amount
            tx_id = f"sim_mint_{len(self._sim_transactions)}"

            if recipient_account:
                self._sim_balances[recipient_account] = self._sim_balances.get(recipient_account, Decimal('0')) + amount

            self._sim_transactions.append({
                'type': 'MINT',
                'amount': str(amount),
                'reason': reason,
                'recipient': recipient_account,
                'timestamp': datetime.utcnow().isoformat()
            })

            return TransactionResult(
                success=True,
                transaction_id=tx_id,
                receipt_status="SUCCESS",
                metadata={'amount_minted': str(amount), 'new_supply': str(self._sim_total_supply)}
            )

        try:
            operator_key = PrivateKey.fromString(self.config.operator_key)
            token_id = TokenId.fromString(self.config.ur_token_id)

            # Mint tokens
            mint_tx = (
                TokenMintTransaction()
                .setTokenId(token_id)
                .setAmount(amount_smallest)
                .freezeWith(self.client)
                .sign(operator_key)
            )

            response = await mint_tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            # If recipient specified, transfer immediately
            if recipient_account and receipt.status == Status.SUCCESS:
                transfer_result = await self.transfer_ur(
                    from_account=self.config.operator_id,
                    to_account=recipient_account,
                    amount=amount,
                    memo=f"Mint distribution: {reason}"
                )
                if not transfer_result.success:
                    logger.warning(f"Mint succeeded but transfer failed: {transfer_result.error}")

            # Log to HCS
            await self._log_to_hcs({
                'action': 'MINT',
                'amount': str(amount),
                'reason': reason,
                'recipient': recipient_account,
                'tx_id': str(response.transactionId)
            })

            return TransactionResult(
                success=True,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'amount_minted': str(amount)}
            )

        except Exception as e:
            logger.error(f"Failed to mint UR: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def burn_ur(
        self,
        amount: Decimal,
        reason: str
    ) -> TransactionResult:
        """
        Burn UR tokens from treasury.

        Args:
            amount: Amount of UR to burn
            reason: Reason for burning (for audit log)
        """
        if not self.config.ur_token_id:
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error="UR token not configured"
            )

        amount_smallest = int(amount * Decimal('100000000'))

        if self._simulation_mode:
            self._sim_total_supply = max(Decimal('0'), self._sim_total_supply - amount)
            tx_id = f"sim_burn_{len(self._sim_transactions)}"

            self._sim_transactions.append({
                'type': 'BURN',
                'amount': str(amount),
                'reason': reason,
                'timestamp': datetime.utcnow().isoformat()
            })

            return TransactionResult(
                success=True,
                transaction_id=tx_id,
                receipt_status="SUCCESS",
                metadata={'amount_burned': str(amount), 'new_supply': str(self._sim_total_supply)}
            )

        try:
            operator_key = PrivateKey.fromString(self.config.operator_key)
            token_id = TokenId.fromString(self.config.ur_token_id)

            burn_tx = (
                TokenBurnTransaction()
                .setTokenId(token_id)
                .setAmount(amount_smallest)
                .freezeWith(self.client)
                .sign(operator_key)
            )

            response = await burn_tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            await self._log_to_hcs({
                'action': 'BURN',
                'amount': str(amount),
                'reason': reason,
                'tx_id': str(response.transactionId)
            })

            return TransactionResult(
                success=True,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'amount_burned': str(amount)}
            )

        except Exception as e:
            logger.error(f"Failed to burn UR: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def transfer_ur(
        self,
        from_account: str,
        to_account: str,
        amount: Decimal,
        memo: Optional[str] = None
    ) -> TransactionResult:
        """
        Transfer UR tokens between accounts.

        Args:
            from_account: Sender's Hedera account ID
            to_account: Recipient's Hedera account ID
            amount: Amount of UR to transfer
            memo: Optional transaction memo
        """
        if not self.config.ur_token_id:
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error="UR token not configured"
            )

        amount_smallest = int(amount * Decimal('100000000'))

        if self._simulation_mode:
            # Check sender balance
            sender_balance = self._sim_balances.get(from_account, Decimal('0'))
            if sender_balance < amount:
                return TransactionResult(
                    success=False,
                    transaction_id=None,
                    receipt_status="INSUFFICIENT_TOKEN_BALANCE",
                    error=f"Insufficient balance: {sender_balance} < {amount}"
                )

            # Execute transfer
            self._sim_balances[from_account] = sender_balance - amount
            self._sim_balances[to_account] = self._sim_balances.get(to_account, Decimal('0')) + amount

            tx_id = f"sim_transfer_{len(self._sim_transactions)}"
            self._sim_transactions.append({
                'type': 'TRANSFER',
                'from': from_account,
                'to': to_account,
                'amount': str(amount),
                'memo': memo,
                'timestamp': datetime.utcnow().isoformat()
            })

            return TransactionResult(
                success=True,
                transaction_id=tx_id,
                receipt_status="SUCCESS",
                metadata={'from': from_account, 'to': to_account, 'amount': str(amount)}
            )

        try:
            token_id = TokenId.fromString(self.config.ur_token_id)
            from_id = AccountId.fromString(from_account)
            to_id = AccountId.fromString(to_account)

            transfer_tx = TransferTransaction()

            if memo:
                transfer_tx.setTransactionMemo(memo)

            transfer_tx.addTokenTransfer(token_id, from_id, -amount_smallest)
            transfer_tx.addTokenTransfer(token_id, to_id, amount_smallest)

            response = await transfer_tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            return TransactionResult(
                success=receipt.status == Status.SUCCESS,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'from': from_account, 'to': to_account, 'amount': str(amount)}
            )

        except Exception as e:
            logger.error(f"Failed to transfer UR: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def get_ur_balance(self, account_id: str) -> Tuple[bool, Decimal, Optional[str]]:
        """
        Get UR token balance for an account.

        Returns:
            Tuple of (success, balance, error_message)
        """
        if not self.config.ur_token_id:
            return (False, Decimal('0'), "UR token not configured")

        if self._simulation_mode:
            balance = self._sim_balances.get(account_id, Decimal('0'))
            return (True, balance, None)

        try:
            account = AccountId.fromString(account_id)
            token_id = TokenId.fromString(self.config.ur_token_id)

            balance_query = await AccountBalanceQuery().setAccountId(account).execute(self.client)
            token_balance = balance_query.tokens.get(token_id, 0)

            # Convert from smallest denomination
            balance = Decimal(token_balance) / Decimal('100000000')
            return (True, balance, None)

        except Exception as e:
            logger.error(f"Failed to get UR balance: {e}")
            return (False, Decimal('0'), str(e))

    async def get_token_info(self) -> Optional[URTokenInfo]:
        """Get information about the UR token"""
        if not self.config.ur_token_id:
            return None

        if self._simulation_mode:
            return URTokenInfo(
                token_id=self.config.ur_token_id or "0.0.SIMULATION",
                name="Unité de Résonance",
                symbol="UR",
                decimals=8,
                total_supply=self._sim_total_supply,
                circulating_supply=sum(self._sim_balances.values()),
                treasury_balance=self._sim_total_supply - sum(self._sim_balances.values()),
                is_paused=False,
                admin_key=None,
                supply_key=None
            )

        try:
            token_id = TokenId.fromString(self.config.ur_token_id)
            info = await TokenInfoQuery().setTokenId(token_id).execute(self.client)

            return URTokenInfo(
                token_id=str(info.tokenId),
                name=info.name,
                symbol=info.symbol,
                decimals=info.decimals,
                total_supply=Decimal(info.totalSupply) / Decimal('100000000'),
                circulating_supply=Decimal('0'),  # Would need to calculate
                treasury_balance=Decimal('0'),  # Would need treasury query
                is_paused=info.pauseStatus,
                admin_key=str(info.adminKey) if info.adminKey else None,
                supply_key=str(info.supplyKey) if info.supplyKey else None
            )

        except Exception as e:
            logger.error(f"Failed to get token info: {e}")
            return None

    # ==================== ACCOUNT OPERATIONS ====================

    async def create_sovereign_account(
        self,
        initial_balance_hbar: Decimal = Decimal('1.0'),
        memo: Optional[str] = None
    ) -> TransactionResult:
        """
        Create a new Hedera account for a sovereign member.

        Args:
            initial_balance_hbar: Initial HBAR balance for gas fees
            memo: Optional account memo

        Returns:
            TransactionResult with account_id and keys in metadata
        """
        if self._simulation_mode:
            account_id = f"0.0.{2000000 + len(self._sim_accounts)}"
            private_key = f"sim_key_{account_id}"
            public_key = f"sim_pub_{account_id}"

            self._sim_accounts[account_id] = {
                'private_key': private_key,
                'public_key': public_key,
                'created_at': datetime.utcnow().isoformat()
            }

            return TransactionResult(
                success=True,
                transaction_id=f"sim_create_account_{len(self._sim_transactions)}",
                receipt_status="SUCCESS",
                metadata={
                    'account_id': account_id,
                    'private_key': private_key,
                    'public_key': public_key
                }
            )

        try:
            # Generate new key pair
            new_key = PrivateKey.generateED25519()
            public_key = new_key.getPublicKey()

            # Create account
            tx = AccountCreateTransaction()
            tx.setKey(public_key)
            tx.setInitialBalance(Hbar.from_(initial_balance_hbar, "hbar"))

            if memo:
                tx.setAccountMemo(memo)

            response = await tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            account_id = str(receipt.accountId)

            # Log creation
            await self._log_to_hcs({
                'action': 'CREATE_ACCOUNT',
                'account_id': account_id,
                'public_key': str(public_key),
                'tx_id': str(response.transactionId)
            })

            return TransactionResult(
                success=True,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={
                    'account_id': account_id,
                    'private_key': str(new_key),
                    'public_key': str(public_key)
                }
            )

        except Exception as e:
            logger.error(f"Failed to create account: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def associate_ur_token(
        self,
        account_id: str,
        account_key: str
    ) -> TransactionResult:
        """
        Associate UR token with an account (required before receiving tokens).

        Args:
            account_id: Hedera account ID to associate
            account_key: Private key for the account
        """
        if not self.config.ur_token_id:
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error="UR token not configured"
            )

        if self._simulation_mode:
            return TransactionResult(
                success=True,
                transaction_id=f"sim_associate_{len(self._sim_transactions)}",
                receipt_status="SUCCESS",
                metadata={'account_id': account_id, 'token_id': self.config.ur_token_id}
            )

        try:
            token_id = TokenId.fromString(self.config.ur_token_id)
            account = AccountId.fromString(account_id)
            key = PrivateKey.fromString(account_key)

            tx = (
                TokenAssociateTransaction()
                .setAccountId(account)
                .setTokenIds([token_id])
                .freezeWith(self.client)
                .sign(key)
            )

            response = await tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            return TransactionResult(
                success=receipt.status == Status.SUCCESS,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'account_id': account_id, 'token_id': self.config.ur_token_id}
            )

        except Exception as e:
            logger.error(f"Failed to associate token: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    # ==================== CONSENSUS SERVICE (HCS) ====================

    async def create_audit_topic(
        self,
        memo: str = "AT·OM Sovereign Economy Audit Log"
    ) -> TransactionResult:
        """
        Create an HCS topic for immutable audit logging.
        """
        if self._simulation_mode:
            topic_id = f"0.0.{3000000 + len(self._sim_transactions)}"
            return TransactionResult(
                success=True,
                transaction_id=f"sim_create_topic_{len(self._sim_transactions)}",
                receipt_status="SUCCESS",
                metadata={'topic_id': topic_id}
            )

        try:
            operator_key = PrivateKey.fromString(self.config.operator_key)

            tx = (
                TopicCreateTransaction()
                .setTopicMemo(memo)
                .setAdminKey(operator_key.getPublicKey())
                .setSubmitKey(operator_key.getPublicKey())
            )

            response = await tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            topic_id = str(receipt.topicId)
            logger.info(f"Created HCS topic: {topic_id}")

            return TransactionResult(
                success=True,
                transaction_id=str(response.transactionId),
                receipt_status=str(receipt.status),
                metadata={'topic_id': topic_id}
            )

        except Exception as e:
            logger.error(f"Failed to create HCS topic: {e}")
            return TransactionResult(
                success=False,
                transaction_id=None,
                receipt_status=None,
                error=str(e)
            )

    async def _log_to_hcs(self, message: Dict[str, Any]) -> bool:
        """
        Submit a message to the HCS audit topic.

        Args:
            message: Dictionary to be logged (will be JSON encoded)
        """
        if not self.config.hcs_topic_id:
            logger.debug("HCS topic not configured, skipping audit log")
            return False

        if self._simulation_mode:
            self._sim_transactions.append({
                'type': 'HCS_MESSAGE',
                'topic_id': self.config.hcs_topic_id,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            })
            return True

        try:
            topic_id = TopicId.fromString(self.config.hcs_topic_id)
            operator_key = PrivateKey.fromString(self.config.operator_key)

            # Add timestamp to message
            message['logged_at'] = datetime.utcnow().isoformat()
            message_bytes = json.dumps(message).encode('utf-8')

            tx = (
                TopicMessageSubmitTransaction()
                .setTopicId(topic_id)
                .setMessage(message_bytes)
                .freezeWith(self.client)
                .sign(operator_key)
            )

            response = await tx.execute(self.client)
            receipt = await response.getReceipt(self.client)

            return receipt.status == Status.SUCCESS

        except Exception as e:
            logger.error(f"Failed to log to HCS: {e}")
            return False

    async def log_governance_action(
        self,
        action_type: str,
        proposal_id: str,
        voter_id: Optional[str] = None,
        vote: Optional[str] = None,
        result: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Log a governance action to HCS for immutable record.
        """
        message = {
            'category': 'GOVERNANCE',
            'action': action_type,
            'proposal_id': proposal_id
        }

        if voter_id:
            message['voter_id'] = voter_id
        if vote:
            message['vote'] = vote
        if result:
            message['result'] = result
        if metadata:
            message['metadata'] = metadata

        return await self._log_to_hcs(message)

    async def log_economic_event(
        self,
        event_type: str,
        amount: Optional[Decimal] = None,
        from_account: Optional[str] = None,
        to_account: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Log an economic event to HCS for audit trail.
        """
        message = {
            'category': 'ECONOMIC',
            'event': event_type
        }

        if amount is not None:
            message['amount'] = str(amount)
        if from_account:
            message['from'] = from_account
        if to_account:
            message['to'] = to_account
        if metadata:
            message['metadata'] = metadata

        return await self._log_to_hcs(message)

    # ==================== UTILITY METHODS ====================

    def get_simulation_state(self) -> Dict[str, Any]:
        """Get current simulation state (for testing/debugging)"""
        if not self._simulation_mode:
            return {'simulation_mode': False}

        return {
            'simulation_mode': True,
            'total_supply': str(self._sim_total_supply),
            'balances': {k: str(v) for k, v in self._sim_balances.items()},
            'accounts': self._sim_accounts,
            'transaction_count': len(self._sim_transactions),
            'recent_transactions': self._sim_transactions[-10:]
        }

    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized

    def is_simulation_mode(self) -> bool:
        """Check if running in simulation mode"""
        return self._simulation_mode


# ==================== SINGLETON INSTANCE ====================

_hedera_service: Optional[HederaService] = None


def get_hedera_service() -> HederaService:
    """Get or create the singleton Hedera service instance"""
    global _hedera_service
    if _hedera_service is None:
        _hedera_service = HederaService()
    return _hedera_service


async def initialize_hedera() -> bool:
    """Initialize the Hedera service"""
    service = get_hedera_service()
    return await service.initialize()
