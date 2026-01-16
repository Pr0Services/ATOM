"""
============================================================================
CHE·NU™ V69 — LIBRARY AUTHOR EQUITY SYSTEM
============================================================================
Spec: GPT1/CHE-NU_LIB_AUTHOR_EQUITY_SYSTEM.md

Objective: Fair, transparent, "participate-native" monetization for authors.

Revenue models (per spec):
1. Tips (per chunk/chapter/book)
2. Micro-licenses (reading, remix, adaptation)
3. Sponsorship (local/enterprise)
4. Scholar Grants (educational content)

Features:
- Wallets & splits
- Trust multipliers
- Autonomous publishing contract (CEA)
- Anti-abuse detection
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from ..models import (
    Wallet,
    TipTransaction,
    SplitConfig,
    AutonomousPublishingContract,
    RevenueType,
    BookArtifact,
    generate_id,
    compute_hash,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# WALLET MANAGER
# ============================================================================

class WalletManager:
    """
    Manage wallets for payments.
    
    Per spec: Wallets & splits
    """
    
    def __init__(self):
        self._wallets: Dict[str, Wallet] = {}
        self._transactions: List[TipTransaction] = []
    
    def create_wallet(
        self,
        owner_id: str,
        owner_type: str = "author",
    ) -> Wallet:
        """Create a wallet"""
        wallet = Wallet(
            wallet_id=generate_id(),
            owner_id=owner_id,
            owner_type=owner_type,
        )
        self._wallets[wallet.wallet_id] = wallet
        return wallet
    
    def get_wallet(self, wallet_id: str) -> Optional[Wallet]:
        """Get wallet by ID"""
        return self._wallets.get(wallet_id)
    
    def get_wallet_by_owner(self, owner_id: str) -> Optional[Wallet]:
        """Get wallet by owner"""
        for wallet in self._wallets.values():
            if wallet.owner_id == owner_id:
                return wallet
        return None
    
    def credit(self, wallet_id: str, amount: float) -> bool:
        """Credit amount to wallet"""
        wallet = self._wallets.get(wallet_id)
        if not wallet:
            return False
        wallet.balance += amount
        return True
    
    def debit(self, wallet_id: str, amount: float) -> bool:
        """Debit amount from wallet"""
        wallet = self._wallets.get(wallet_id)
        if not wallet or wallet.balance < amount:
            return False
        wallet.balance -= amount
        return True
    
    def transfer(
        self,
        from_wallet_id: str,
        to_wallet_id: str,
        amount: float,
    ) -> bool:
        """Transfer between wallets"""
        if not self.debit(from_wallet_id, amount):
            return False
        if not self.credit(to_wallet_id, amount):
            # Rollback
            self.credit(from_wallet_id, amount)
            return False
        return True


# ============================================================================
# TIP SERVICE
# ============================================================================

class TipService:
    """
    Handle tips for books and chunks.
    
    Per spec: Tips (par chunk / chapitre / livre)
    """
    
    def __init__(self, wallet_manager: WalletManager):
        self.wallets = wallet_manager
        self._tips: List[TipTransaction] = []
        
        # Anti-abuse tracking
        self._tip_counts: Dict[str, Dict[str, int]] = {}  # from_wallet → {book_id: count}
        self._rate_limits: Dict[str, int] = {}  # wallet_id → tips today
    
    def send_tip(
        self,
        from_wallet_id: str,
        to_wallet_id: str,
        book_id: str,
        amount: float,
        chunk_id: str = None,
    ) -> Optional[TipTransaction]:
        """
        Send a tip.
        
        Per spec: Paiement en $CHE-NU, aucun intermédiaire
        """
        # Anti-abuse check
        if not self._check_rate_limit(from_wallet_id):
            logger.warning(f"Rate limit exceeded for wallet {from_wallet_id}")
            return None
        
        if not self._check_farm_detection(from_wallet_id, book_id):
            logger.warning(f"Tip farm detected for wallet {from_wallet_id}")
            return None
        
        # Transfer
        if not self.wallets.transfer(from_wallet_id, to_wallet_id, amount):
            return None
        
        # Record transaction
        tx = TipTransaction(
            tx_id=generate_id(),
            from_wallet=from_wallet_id,
            to_wallet=to_wallet_id,
            book_id=book_id,
            chunk_id=chunk_id,
            amount=amount,
        )
        
        self._tips.append(tx)
        self._update_tracking(from_wallet_id, book_id)
        
        logger.info(f"Tip {tx.tx_id}: {amount} CHE-NU for book {book_id}")
        return tx
    
    def _check_rate_limit(self, wallet_id: str, max_per_day: int = 100) -> bool:
        """Check rate limit"""
        count = self._rate_limits.get(wallet_id, 0)
        return count < max_per_day
    
    def _check_farm_detection(
        self,
        wallet_id: str,
        book_id: str,
        max_per_book: int = 10,
    ) -> bool:
        """
        Detect tip farming.
        
        Per spec anti-abuse: détection de farm de tips
        """
        if wallet_id not in self._tip_counts:
            return True
        
        book_count = self._tip_counts[wallet_id].get(book_id, 0)
        return book_count < max_per_book
    
    def _update_tracking(self, wallet_id: str, book_id: str) -> None:
        """Update tracking for anti-abuse"""
        self._rate_limits[wallet_id] = self._rate_limits.get(wallet_id, 0) + 1
        
        if wallet_id not in self._tip_counts:
            self._tip_counts[wallet_id] = {}
        self._tip_counts[wallet_id][book_id] = self._tip_counts[wallet_id].get(book_id, 0) + 1
    
    def get_tips_for_book(self, book_id: str) -> List[TipTransaction]:
        """Get all tips for a book"""
        return [t for t in self._tips if t.book_id == book_id]
    
    def get_total_tips(self, book_id: str) -> float:
        """Get total tips for a book"""
        return sum(t.amount for t in self._tips if t.book_id == book_id)


# ============================================================================
# REVENUE DISTRIBUTOR
# ============================================================================

class RevenueDistributor:
    """
    Distribute revenue according to splits.
    
    Per spec: author_wallet, collaborator_wallets, platform_fee, community_fund
    """
    
    def __init__(self, wallet_manager: WalletManager):
        self.wallets = wallet_manager
        
        # System wallets
        self.platform_wallet: Optional[str] = None
        self.community_wallet: Optional[str] = None
    
    def setup_system_wallets(
        self,
        platform_wallet_id: str,
        community_wallet_id: str,
    ) -> None:
        """Setup system wallets"""
        self.platform_wallet = platform_wallet_id
        self.community_wallet = community_wallet_id
    
    def distribute(
        self,
        amount: float,
        author_wallet_id: str,
        split_config: SplitConfig,
        collaborator_wallets: Dict[str, str] = None,
    ) -> Dict[str, float]:
        """
        Distribute revenue according to splits.
        
        Returns dict of wallet_id → amount distributed
        """
        collaborator_wallets = collaborator_wallets or {}
        distributions = {}
        
        # Calculate amounts
        author_amount = amount * split_config.author_split
        platform_amount = amount * split_config.platform_fee
        community_amount = amount * split_config.community_fund
        
        # Collaborator amounts
        collaborator_total = sum(split_config.collaborator_splits.values())
        remaining = amount - author_amount - platform_amount - community_amount
        
        # Credit author
        self.wallets.credit(author_wallet_id, author_amount)
        distributions[author_wallet_id] = author_amount
        
        # Credit collaborators
        for collab_id, split in split_config.collaborator_splits.items():
            if collab_id in collaborator_wallets:
                collab_amount = remaining * (split / collaborator_total) if collaborator_total > 0 else 0
                self.wallets.credit(collaborator_wallets[collab_id], collab_amount)
                distributions[collaborator_wallets[collab_id]] = collab_amount
        
        # Credit platform
        if self.platform_wallet:
            self.wallets.credit(self.platform_wallet, platform_amount)
            distributions[self.platform_wallet] = platform_amount
        
        # Credit community
        if self.community_wallet:
            self.wallets.credit(self.community_wallet, community_amount)
            distributions[self.community_wallet] = community_amount
        
        logger.info(f"Distributed {amount} CHE-NU across {len(distributions)} wallets")
        return distributions


# ============================================================================
# CONTRACT MANAGER
# ============================================================================

class ContractManager:
    """
    Manage autonomous publishing contracts (CEA).
    
    Per spec: Contrat d'édition autonome
    """
    
    def __init__(self):
        self._contracts: Dict[str, AutonomousPublishingContract] = {}
    
    def create_contract(
        self,
        book_id: str,
        author_id: str,
        rights: List[str] = None,
        split_config: SplitConfig = None,
        content_policy: str = "",
    ) -> AutonomousPublishingContract:
        """
        Create autonomous publishing contract.
        
        Per spec artifact: signed contract defining exact rights
        """
        contract = AutonomousPublishingContract(
            contract_id=generate_id(),
            book_id=book_id,
            author_id=author_id,
            rights_granted=rights or ["read", "share"],
            split_config=split_config or SplitConfig(),
            content_policy=content_policy,
            withdrawal_conditions={
                "notice_days": 30,
                "revenue_settlement": "immediate",
            },
        )
        
        # Sign contract
        contract.signature = sign_artifact({
            "contract_id": contract.contract_id,
            "book_id": book_id,
            "author_id": author_id,
            "rights": contract.rights_granted,
        }, author_id)
        
        self._contracts[contract.contract_id] = contract
        
        logger.info(f"Created contract {contract.contract_id} for book {book_id}")
        return contract
    
    def get_contract(self, contract_id: str) -> Optional[AutonomousPublishingContract]:
        """Get contract by ID"""
        return self._contracts.get(contract_id)
    
    def get_contract_for_book(self, book_id: str) -> Optional[AutonomousPublishingContract]:
        """Get contract for a book"""
        for contract in self._contracts.values():
            if contract.book_id == book_id:
                return contract
        return None
    
    def verify_contract(self, contract: AutonomousPublishingContract) -> bool:
        """Verify contract signature"""
        expected = sign_artifact({
            "contract_id": contract.contract_id,
            "book_id": contract.book_id,
            "author_id": contract.author_id,
            "rights": contract.rights_granted,
        }, contract.author_id)
        
        return contract.signature == expected


# ============================================================================
# TRUST MULTIPLIER
# ============================================================================

class TrustMultiplier:
    """
    Apply trust score multipliers.
    
    Per spec: Trust multipliers (optionnels)
    - Débloquer visibilité additionnelle
    - Qualifier pour sponsorships
    - NE doit PAS censurer
    """
    
    VISIBILITY_THRESHOLD = 0.7
    SPONSORSHIP_THRESHOLD = 0.8
    
    def __init__(self):
        self._trust_scores: Dict[str, float] = {}
    
    def set_trust_score(self, author_id: str, score: float) -> None:
        """Set author trust score"""
        self._trust_scores[author_id] = max(0, min(1, score))
    
    def get_trust_score(self, author_id: str) -> float:
        """Get author trust score"""
        return self._trust_scores.get(author_id, 0.5)
    
    def qualifies_for_visibility_boost(self, author_id: str) -> bool:
        """Check if author qualifies for visibility boost"""
        return self.get_trust_score(author_id) >= self.VISIBILITY_THRESHOLD
    
    def qualifies_for_sponsorship(self, author_id: str) -> bool:
        """Check if author qualifies for sponsorship"""
        return self.get_trust_score(author_id) >= self.SPONSORSHIP_THRESHOLD
    
    def get_multiplier(self, author_id: str) -> float:
        """Get revenue multiplier based on trust"""
        score = self.get_trust_score(author_id)
        # Linear multiplier: 1.0 at 0.5 trust, up to 1.2 at 1.0 trust
        return 1.0 + (score - 0.5) * 0.4


# ============================================================================
# AUTHOR EQUITY SYSTEM
# ============================================================================

class AuthorEquitySystem:
    """
    Main system for author monetization.
    """
    
    def __init__(self):
        self.wallets = WalletManager()
        self.tips = TipService(self.wallets)
        self.distributor = RevenueDistributor(self.wallets)
        self.contracts = ContractManager()
        self.trust = TrustMultiplier()
        
        # Setup system wallets
        platform_wallet = self.wallets.create_wallet("platform", "platform")
        community_wallet = self.wallets.create_wallet("community", "community")
        self.distributor.setup_system_wallets(
            platform_wallet.wallet_id,
            community_wallet.wallet_id,
        )
    
    def register_author(self, author_id: str) -> Wallet:
        """Register author and create wallet"""
        return self.wallets.create_wallet(author_id, "author")
    
    def setup_book(
        self,
        book_id: str,
        author_id: str,
        rights: List[str] = None,
        split_config: SplitConfig = None,
    ) -> Tuple[Wallet, AutonomousPublishingContract]:
        """Setup book with contract and wallet"""
        # Get or create author wallet
        wallet = self.wallets.get_wallet_by_owner(author_id)
        if not wallet:
            wallet = self.register_author(author_id)
        
        # Create contract
        contract = self.contracts.create_contract(
            book_id=book_id,
            author_id=author_id,
            rights=rights,
            split_config=split_config,
        )
        
        return wallet, contract
    
    def process_tip(
        self,
        from_user_id: str,
        book_id: str,
        amount: float,
        chunk_id: str = None,
    ) -> Optional[TipTransaction]:
        """Process a tip for a book"""
        # Get sender wallet
        from_wallet = self.wallets.get_wallet_by_owner(from_user_id)
        if not from_wallet:
            from_wallet = self.wallets.create_wallet(from_user_id, "reader")
            # Need to fund wallet first in production
            self.wallets.credit(from_wallet.wallet_id, 1000)  # Mock funding
        
        # Get contract to find author
        contract = self.contracts.get_contract_for_book(book_id)
        if not contract:
            logger.warning(f"No contract found for book {book_id}")
            return None
        
        # Get author wallet
        to_wallet = self.wallets.get_wallet_by_owner(contract.author_id)
        if not to_wallet:
            logger.warning(f"No wallet found for author {contract.author_id}")
            return None
        
        # Apply trust multiplier
        multiplier = self.trust.get_multiplier(contract.author_id)
        effective_amount = amount * multiplier
        
        # Send tip
        tx = self.tips.send_tip(
            from_wallet.wallet_id,
            to_wallet.wallet_id,
            book_id,
            effective_amount,
            chunk_id,
        )
        
        return tx
    
    def get_author_dashboard(self, author_id: str) -> Dict[str, Any]:
        """
        Get author dashboard data.
        
        Per spec: Dashboard auteur: revenus + droits + versions
        """
        wallet = self.wallets.get_wallet_by_owner(author_id)
        
        # Get all contracts
        author_contracts = [
            c for c in self.contracts._contracts.values()
            if c.author_id == author_id
        ]
        
        # Get all tips
        author_tips = []
        for contract in author_contracts:
            book_tips = self.tips.get_tips_for_book(contract.book_id)
            author_tips.extend(book_tips)
        
        return {
            "author_id": author_id,
            "wallet_balance": wallet.balance if wallet else 0,
            "trust_score": self.trust.get_trust_score(author_id),
            "qualifies_sponsorship": self.trust.qualifies_for_sponsorship(author_id),
            "books": len(author_contracts),
            "total_tips_received": sum(t.amount for t in author_tips),
            "tip_count": len(author_tips),
            "contracts": [
                {
                    "contract_id": c.contract_id,
                    "book_id": c.book_id,
                    "rights": c.rights_granted,
                }
                for c in author_contracts
            ],
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_equity_system() -> AuthorEquitySystem:
    """Create author equity system"""
    return AuthorEquitySystem()


def create_split_config(
    author_split: float = 0.85,
    platform_fee: float = 0.05,
    community_fund: float = 0.10,
) -> SplitConfig:
    """Create split configuration"""
    return SplitConfig(
        author_split=author_split,
        platform_fee=platform_fee,
        community_fund=community_fund,
    )
