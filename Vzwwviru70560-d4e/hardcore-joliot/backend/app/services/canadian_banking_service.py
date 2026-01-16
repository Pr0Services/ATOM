"""
CHE·NU Canadian Banking Service V72

Open Banking integration for Canadian financial institutions using:
- Flinks (Primary aggregator for Canadian banks)
- Direct bank APIs (for supported institutions)

Supported Banks:
- Desjardins (Mouvement Desjardins)
- TD Canada Trust
- RBC Banque Royale
- BMO Bank of Montreal
- Scotiabank
- CIBC
- National Bank (Banque Nationale)
- Tangerine

@version V72.0
@phase Phase 2 - Financial Integrations
"""

import os
import secrets
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
import urllib.parse
import base64
import logging

logger = logging.getLogger(__name__)


# ==============================================================================
# ENUMS
# ==============================================================================

class CanadianBank(Enum):
    """Supported Canadian banking institutions."""
    DESJARDINS = "desjardins"
    TD = "td_bank"
    RBC = "rbc"
    BMO = "bmo"
    SCOTIABANK = "scotiabank"
    CIBC = "cibc"
    NATIONAL_BANK = "national_bank"
    TANGERINE = "tangerine"


class BankConnectionStatus(Enum):
    """Bank connection status."""
    PENDING = "pending"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    REQUIRES_MFA = "requires_mfa"
    EXPIRED = "expired"


class AccountType(Enum):
    """Bank account types."""
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    LINE_OF_CREDIT = "line_of_credit"
    MORTGAGE = "mortgage"
    INVESTMENT = "investment"
    RRSP = "rrsp"
    TFSA = "tfsa"
    GIC = "gic"
    LOAN = "loan"


class TransactionCategory(Enum):
    """Transaction categories."""
    INCOME = "income"
    SALARY = "salary"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    PURCHASE = "purchase"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    FEE = "fee"
    INTEREST = "interest"
    REFUND = "refund"
    OTHER = "other"


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass
class BankConfig:
    """Configuration for a specific bank."""
    bank_id: CanadianBank
    name: str
    name_fr: str
    icon: str
    color: str
    flinks_institution_id: str
    supports_direct_api: bool = False
    oauth_enabled: bool = False
    mfa_required: bool = True


@dataclass
class BankAccount:
    """Bank account information."""
    id: str
    user_id: str
    bank_id: CanadianBank
    account_number_masked: str
    account_type: AccountType
    currency: str
    balance: float
    available_balance: float
    account_name: str
    institution_name: str
    last_refreshed: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BankTransaction:
    """Bank transaction record."""
    id: str
    account_id: str
    date: datetime
    description: str
    amount: float
    currency: str
    category: TransactionCategory
    merchant: Optional[str]
    pending: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BankConnection:
    """Bank connection state."""
    id: str
    user_id: str
    bank_id: CanadianBank
    status: BankConnectionStatus
    flinks_login_id: Optional[str]
    last_sync: Optional[datetime]
    accounts: List[str]  # Account IDs
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlinksSession:
    """Flinks connection session."""
    session_id: str
    user_id: str
    bank_id: CanadianBank
    redirect_url: str
    state: str
    created_at: datetime
    expires_at: datetime


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class CanadianBankingConfig:
    """Canadian banking configuration."""

    # Flinks API Configuration
    FLINKS_CUSTOMER_ID: str = os.getenv("FLINKS_CUSTOMER_ID", "")
    FLINKS_API_KEY: str = os.getenv("FLINKS_API_KEY", "")
    FLINKS_API_URL: str = os.getenv("FLINKS_API_URL", "https://toolbox-api.private.fin.ag")
    FLINKS_IFRAME_URL: str = os.getenv("FLINKS_IFRAME_URL", "https://toolbox.private.fin.ag")
    FLINKS_ENV: str = os.getenv("FLINKS_ENV", "sandbox")  # sandbox | production

    # Redirect URIs
    REDIRECT_URI: str = os.getenv("BANKING_REDIRECT_URI", "http://localhost:3000/banking/callback")

    # Security
    SESSION_EXPIRY_MINUTES: int = 15
    TOKEN_ENCRYPTION_KEY: str = os.getenv("BANKING_ENCRYPTION_KEY", "")

    # Sync settings
    AUTO_REFRESH_ENABLED: bool = True
    REFRESH_INTERVAL_HOURS: int = 4
    TRANSACTION_HISTORY_DAYS: int = 90


# Bank configurations (Flinks institution IDs)
CANADIAN_BANKS: Dict[CanadianBank, BankConfig] = {
    CanadianBank.DESJARDINS: BankConfig(
        bank_id=CanadianBank.DESJARDINS,
        name="Desjardins",
        name_fr="Mouvement Desjardins",
        icon="",
        color="#00874e",
        flinks_institution_id="desjardins",
        mfa_required=True
    ),
    CanadianBank.TD: BankConfig(
        bank_id=CanadianBank.TD,
        name="TD Canada Trust",
        name_fr="TD Canada Trust",
        icon="",
        color="#34a853",
        flinks_institution_id="td",
        mfa_required=True
    ),
    CanadianBank.RBC: BankConfig(
        bank_id=CanadianBank.RBC,
        name="RBC Royal Bank",
        name_fr="RBC Banque Royale",
        icon="",
        color="#0051a5",
        flinks_institution_id="rbc",
        mfa_required=True
    ),
    CanadianBank.BMO: BankConfig(
        bank_id=CanadianBank.BMO,
        name="BMO Bank of Montreal",
        name_fr="BMO Banque de Montreal",
        icon="",
        color="#0079c1",
        flinks_institution_id="bmo",
        mfa_required=True
    ),
    CanadianBank.SCOTIABANK: BankConfig(
        bank_id=CanadianBank.SCOTIABANK,
        name="Scotiabank",
        name_fr="Banque Scotia",
        icon="",
        color="#ec111a",
        flinks_institution_id="scotiabank",
        mfa_required=True
    ),
    CanadianBank.CIBC: BankConfig(
        bank_id=CanadianBank.CIBC,
        name="CIBC",
        name_fr="Banque CIBC",
        icon="",
        color="#bb0628",
        flinks_institution_id="cibc",
        mfa_required=True
    ),
    CanadianBank.NATIONAL_BANK: BankConfig(
        bank_id=CanadianBank.NATIONAL_BANK,
        name="National Bank",
        name_fr="Banque Nationale",
        icon="",
        color="#e31837",
        flinks_institution_id="nbc",
        mfa_required=True
    ),
    CanadianBank.TANGERINE: BankConfig(
        bank_id=CanadianBank.TANGERINE,
        name="Tangerine",
        name_fr="Tangerine",
        icon="",
        color="#ff6600",
        flinks_institution_id="tangerine",
        mfa_required=True
    ),
}


# ==============================================================================
# HTTP CLIENT (Use httpx/aiohttp in production)
# ==============================================================================

class FlinksHTTPClient:
    """
    HTTP client for Flinks API.
    In production, use httpx or aiohttp for async support.
    """

    def __init__(self):
        self.base_url = CanadianBankingConfig.FLINKS_API_URL
        self.customer_id = CanadianBankingConfig.FLINKS_CUSTOMER_ID
        self.api_key = CanadianBankingConfig.FLINKS_API_KEY

    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authentication."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "x-customer-id": self.customer_id
        }

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request to Flinks API."""
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        logger.info(f"[Flinks] POST {url}")

        # Mock response for development
        # In production: httpx.post(url, json=data, headers=headers).json()
        return self._mock_response(endpoint, data)

    def get(self, endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET request to Flinks API."""
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        logger.info(f"[Flinks] GET {url}")

        # Mock response for development
        return self._mock_response(endpoint, params or {})

    def _mock_response(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock Flinks API responses for development."""

        if "Authorize" in endpoint:
            return {
                "RequestId": str(uuid4()),
                "Login": {
                    "Id": f"login_{secrets.token_hex(8)}",
                    "Username": "user@example.com"
                },
                "Institution": data.get("Institution", "desjardins"),
                "HttpStatusCode": 200,
                "Links": {
                    "self": f"{self.base_url}/Authorize"
                }
            }

        elif "GetAccountsSummary" in endpoint:
            return {
                "RequestId": str(uuid4()),
                "Accounts": [
                    {
                        "Id": str(uuid4()),
                        "TransitNumber": "12345",
                        "InstitutionNumber": "815",
                        "AccountNumber": "****1234",
                        "Title": "Compte Cheques",
                        "Category": "Operations",
                        "Type": "Checking",
                        "Currency": "CAD",
                        "Balance": {
                            "Current": 5234.56,
                            "Available": 5234.56
                        }
                    },
                    {
                        "Id": str(uuid4()),
                        "TransitNumber": "12345",
                        "InstitutionNumber": "815",
                        "AccountNumber": "****5678",
                        "Title": "Compte Epargne",
                        "Category": "Operations",
                        "Type": "Savings",
                        "Currency": "CAD",
                        "Balance": {
                            "Current": 15000.00,
                            "Available": 15000.00
                        }
                    },
                    {
                        "Id": str(uuid4()),
                        "AccountNumber": "****9012",
                        "Title": "CELI",
                        "Category": "Investment",
                        "Type": "TFSA",
                        "Currency": "CAD",
                        "Balance": {
                            "Current": 45000.00,
                            "Available": 45000.00
                        }
                    }
                ],
                "HttpStatusCode": 200
            }

        elif "GetAccountsDetail" in endpoint:
            return {
                "RequestId": str(uuid4()),
                "Accounts": [
                    {
                        "Id": data.get("AccountId", str(uuid4())),
                        "Transactions": [
                            {
                                "Id": str(uuid4()),
                                "Date": (datetime.now() - timedelta(days=1)).isoformat(),
                                "Description": "INTERAC VIREMENT",
                                "Debit": 0,
                                "Credit": 2500.00,
                                "Balance": 5234.56
                            },
                            {
                                "Id": str(uuid4()),
                                "Date": (datetime.now() - timedelta(days=2)).isoformat(),
                                "Description": "METRO EPICERIE",
                                "Debit": 156.78,
                                "Credit": 0,
                                "Balance": 2734.56
                            },
                            {
                                "Id": str(uuid4()),
                                "Date": (datetime.now() - timedelta(days=3)).isoformat(),
                                "Description": "PAIEMENT HYDRO-QUEBEC",
                                "Debit": 89.45,
                                "Credit": 0,
                                "Balance": 2891.34
                            },
                            {
                                "Id": str(uuid4()),
                                "Date": (datetime.now() - timedelta(days=5)).isoformat(),
                                "Description": "SALAIRE EMPLOYEUR INC",
                                "Debit": 0,
                                "Credit": 3500.00,
                                "Balance": 2980.79
                            }
                        ]
                    }
                ],
                "HttpStatusCode": 200
            }

        elif "DeleteCard" in endpoint:
            return {
                "RequestId": str(uuid4()),
                "HttpStatusCode": 200,
                "Message": "Card deleted successfully"
            }

        return {"HttpStatusCode": 200}


flinks_client = FlinksHTTPClient()


# ==============================================================================
# CANADIAN BANKING SERVICE
# ==============================================================================

class CanadianBankingService:
    """
    Canadian Banking Service.

    Provides Open Banking functionality for Canadian financial institutions
    using Flinks as the primary aggregator.
    """

    def __init__(self):
        self._sessions: Dict[str, FlinksSession] = {}  # In production: Redis
        self._connections: Dict[str, BankConnection] = {}  # In production: Database
        self._accounts: Dict[str, BankAccount] = {}  # In production: Database
        self._transactions: Dict[str, List[BankTransaction]] = {}  # In production: Database

    # --------------------------------------------------------------------------
    # Bank Configuration
    # --------------------------------------------------------------------------

    def get_supported_banks(self) -> List[Dict[str, Any]]:
        """Get list of all supported Canadian banks."""
        return [
            {
                "id": config.bank_id.value,
                "name": config.name,
                "name_fr": config.name_fr,
                "icon": config.icon,
                "color": config.color,
                "mfa_required": config.mfa_required
            }
            for config in CANADIAN_BANKS.values()
        ]

    def get_bank_config(self, bank_id: CanadianBank) -> Optional[BankConfig]:
        """Get configuration for a specific bank."""
        return CANADIAN_BANKS.get(bank_id)

    # --------------------------------------------------------------------------
    # Connection Flow
    # --------------------------------------------------------------------------

    def initiate_connection(
        self,
        user_id: str,
        bank_id: CanadianBank,
        redirect_uri: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Initiate bank connection flow.

        Returns:
            Tuple of (iframe_url, session_state)
        """
        bank_config = self.get_bank_config(bank_id)
        if not bank_config:
            raise ValueError(f"Unsupported bank: {bank_id}")

        # Generate session state for CSRF protection
        state = secrets.token_urlsafe(32)
        session_id = str(uuid4())

        # Build Flinks iframe URL
        redirect = redirect_uri or CanadianBankingConfig.REDIRECT_URI

        iframe_params = {
            "customerId": CanadianBankingConfig.FLINKS_CUSTOMER_ID,
            "institution": bank_config.flinks_institution_id,
            "demo": "true" if CanadianBankingConfig.FLINKS_ENV == "sandbox" else "false",
            "redirectUrl": redirect,
            "state": state,
            "tag": user_id,  # Associate with user
            "language": "fr",  # French for Quebec users
            "desktopLayout": "true",
            "features": "AccountSelection"
        }

        iframe_url = f"{CanadianBankingConfig.FLINKS_IFRAME_URL}?{urllib.parse.urlencode(iframe_params)}"

        # Store session
        now = datetime.utcnow()
        session = FlinksSession(
            session_id=session_id,
            user_id=user_id,
            bank_id=bank_id,
            redirect_url=redirect,
            state=state,
            created_at=now,
            expires_at=now + timedelta(minutes=CanadianBankingConfig.SESSION_EXPIRY_MINUTES)
        )
        self._sessions[state] = session

        logger.info(f"Initiated bank connection for user {user_id} to {bank_id.value}")

        return iframe_url, state

    def complete_connection(
        self,
        state: str,
        login_id: str,
        institution: str
    ) -> BankConnection:
        """
        Complete bank connection after Flinks callback.

        Args:
            state: Session state from callback
            login_id: Flinks login ID
            institution: Institution code

        Returns:
            BankConnection object
        """
        # Verify state
        session = self._sessions.pop(state, None)
        if not session:
            raise ValueError("Invalid or expired session state")

        if datetime.utcnow() > session.expires_at:
            raise ValueError("Session has expired")

        # Create connection record
        now = datetime.utcnow()
        connection_id = str(uuid4())

        connection = BankConnection(
            id=connection_id,
            user_id=session.user_id,
            bank_id=session.bank_id,
            status=BankConnectionStatus.CONNECTED,
            flinks_login_id=login_id,
            last_sync=now,
            accounts=[],
            created_at=now,
            updated_at=now
        )

        self._connections[connection_id] = connection

        logger.info(f"Completed bank connection {connection_id} for user {session.user_id}")

        # Fetch accounts
        self._sync_accounts(connection)

        return connection

    # --------------------------------------------------------------------------
    # Account Operations
    # --------------------------------------------------------------------------

    def _sync_accounts(self, connection: BankConnection) -> List[BankAccount]:
        """Sync accounts from Flinks."""
        if not connection.flinks_login_id:
            return []

        response = flinks_client.post(
            f"v3/{CanadianBankingConfig.FLINKS_CUSTOMER_ID}/BankingServices/GetAccountsSummary",
            {"RequestId": connection.flinks_login_id}
        )

        accounts = []
        account_ids = []

        for acc_data in response.get("Accounts", []):
            account_id = acc_data.get("Id", str(uuid4()))

            # Map account type
            acc_type_str = acc_data.get("Type", "Checking").upper()
            account_type = AccountType.CHECKING
            if "SAVING" in acc_type_str:
                account_type = AccountType.SAVINGS
            elif "CREDIT" in acc_type_str:
                account_type = AccountType.CREDIT_CARD
            elif "TFSA" in acc_type_str or "CELI" in acc_type_str:
                account_type = AccountType.TFSA
            elif "RRSP" in acc_type_str or "REER" in acc_type_str:
                account_type = AccountType.RRSP
            elif "MORTGAGE" in acc_type_str or "HYPOTHEQUE" in acc_type_str:
                account_type = AccountType.MORTGAGE
            elif "INVESTMENT" in acc_type_str or "PLACEMENT" in acc_type_str:
                account_type = AccountType.INVESTMENT

            balance_data = acc_data.get("Balance", {})

            account = BankAccount(
                id=account_id,
                user_id=connection.user_id,
                bank_id=connection.bank_id,
                account_number_masked=acc_data.get("AccountNumber", "****"),
                account_type=account_type,
                currency=acc_data.get("Currency", "CAD"),
                balance=balance_data.get("Current", 0.0),
                available_balance=balance_data.get("Available", 0.0),
                account_name=acc_data.get("Title", "Account"),
                institution_name=CANADIAN_BANKS[connection.bank_id].name,
                last_refreshed=datetime.utcnow(),
                metadata=acc_data
            )

            self._accounts[account_id] = account
            accounts.append(account)
            account_ids.append(account_id)

        # Update connection with account IDs
        connection.accounts = account_ids
        connection.last_sync = datetime.utcnow()
        connection.updated_at = datetime.utcnow()

        logger.info(f"Synced {len(accounts)} accounts for connection {connection.id}")

        return accounts

    def get_accounts(self, user_id: str) -> List[BankAccount]:
        """Get all bank accounts for a user."""
        return [
            acc for acc in self._accounts.values()
            if acc.user_id == user_id
        ]

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        """Get specific bank account."""
        return self._accounts.get(account_id)

    def refresh_accounts(self, user_id: str) -> List[BankAccount]:
        """Refresh all accounts for a user."""
        accounts = []

        for connection in self._connections.values():
            if connection.user_id == user_id and connection.status == BankConnectionStatus.CONNECTED:
                accounts.extend(self._sync_accounts(connection))

        return accounts

    # --------------------------------------------------------------------------
    # Transaction Operations
    # --------------------------------------------------------------------------

    def get_transactions(
        self,
        account_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[BankTransaction]:
        """Get transactions for an account."""
        account = self._accounts.get(account_id)
        if not account:
            return []

        # Find connection for this account
        connection = None
        for conn in self._connections.values():
            if account_id in conn.accounts:
                connection = conn
                break

        if not connection or not connection.flinks_login_id:
            return []

        # Fetch from Flinks
        response = flinks_client.post(
            f"v3/{CanadianBankingConfig.FLINKS_CUSTOMER_ID}/BankingServices/GetAccountsDetail",
            {
                "RequestId": connection.flinks_login_id,
                "AccountId": account_id,
                "MostRecent": True,
                "MostRecentCached": True
            }
        )

        transactions = []

        for acc_data in response.get("Accounts", []):
            for tx_data in acc_data.get("Transactions", []):
                # Parse transaction
                debit = tx_data.get("Debit", 0)
                credit = tx_data.get("Credit", 0)
                amount = credit - debit

                # Categorize transaction
                desc = tx_data.get("Description", "").upper()
                category = self._categorize_transaction(desc, amount)

                transaction = BankTransaction(
                    id=tx_data.get("Id", str(uuid4())),
                    account_id=account_id,
                    date=datetime.fromisoformat(tx_data.get("Date", datetime.now().isoformat()).replace("Z", "")),
                    description=tx_data.get("Description", ""),
                    amount=amount,
                    currency=account.currency,
                    category=category,
                    merchant=self._extract_merchant(desc),
                    pending=tx_data.get("Pending", False),
                    metadata=tx_data
                )
                transactions.append(transaction)

        # Store transactions
        self._transactions[account_id] = transactions

        # Apply filters
        if start_date:
            transactions = [t for t in transactions if t.date >= start_date]
        if end_date:
            transactions = [t for t in transactions if t.date <= end_date]

        return transactions[:limit]

    def _categorize_transaction(self, description: str, amount: float) -> TransactionCategory:
        """Categorize a transaction based on description and amount."""
        desc_upper = description.upper()

        if amount > 0:
            if "SALAIRE" in desc_upper or "SALARY" in desc_upper or "PAIE" in desc_upper:
                return TransactionCategory.SALARY
            elif "VIREMENT" in desc_upper or "TRANSFER" in desc_upper:
                return TransactionCategory.TRANSFER
            elif "INTERET" in desc_upper or "INTEREST" in desc_upper:
                return TransactionCategory.INTEREST
            elif "REMBOURSEMENT" in desc_upper or "REFUND" in desc_upper:
                return TransactionCategory.REFUND
            else:
                return TransactionCategory.INCOME
        else:
            if "PAIEMENT" in desc_upper or "PAYMENT" in desc_upper:
                return TransactionCategory.PAYMENT
            elif "RETRAIT" in desc_upper or "WITHDRAWAL" in desc_upper or "ATM" in desc_upper:
                return TransactionCategory.WITHDRAWAL
            elif "FRAIS" in desc_upper or "FEE" in desc_upper:
                return TransactionCategory.FEE
            elif "VIREMENT" in desc_upper or "TRANSFER" in desc_upper:
                return TransactionCategory.TRANSFER
            else:
                return TransactionCategory.PURCHASE

    def _extract_merchant(self, description: str) -> Optional[str]:
        """Extract merchant name from transaction description."""
        # Common patterns in Canadian bank descriptions
        # Format: "MERCHANT LOCATION" or "INTERAC MERCHANT"
        parts = description.split()

        # Skip common prefixes
        skip_words = {"INTERAC", "VIREMENT", "PAIEMENT", "RETRAIT", "ACHAT", "POS", "EFT", "PAD"}
        filtered = [p for p in parts if p.upper() not in skip_words]

        if filtered:
            return " ".join(filtered[:3])  # First 3 words as merchant
        return None

    # --------------------------------------------------------------------------
    # Connection Management
    # --------------------------------------------------------------------------

    def get_connections(self, user_id: str) -> List[BankConnection]:
        """Get all bank connections for a user."""
        return [
            conn for conn in self._connections.values()
            if conn.user_id == user_id
        ]

    def get_connection(self, connection_id: str) -> Optional[BankConnection]:
        """Get specific bank connection."""
        return self._connections.get(connection_id)

    def disconnect_bank(self, user_id: str, connection_id: str) -> bool:
        """Disconnect a bank connection."""
        connection = self._connections.get(connection_id)

        if not connection or connection.user_id != user_id:
            return False

        # Delete from Flinks if possible
        if connection.flinks_login_id:
            try:
                flinks_client.post(
                    f"v3/{CanadianBankingConfig.FLINKS_CUSTOMER_ID}/BankingServices/DeleteCard",
                    {"LoginId": connection.flinks_login_id}
                )
            except Exception as e:
                logger.warning(f"Failed to delete Flinks card: {e}")

        # Remove accounts
        for account_id in connection.accounts:
            self._accounts.pop(account_id, None)
            self._transactions.pop(account_id, None)

        # Update connection status
        connection.status = BankConnectionStatus.DISCONNECTED
        connection.updated_at = datetime.utcnow()

        logger.info(f"Disconnected bank connection {connection_id} for user {user_id}")

        return True

    # --------------------------------------------------------------------------
    # Aggregated Data
    # --------------------------------------------------------------------------

    def get_total_balance(self, user_id: str) -> Dict[str, float]:
        """Get total balance across all accounts by currency."""
        totals: Dict[str, float] = {}

        for account in self.get_accounts(user_id):
            currency = account.currency
            if currency not in totals:
                totals[currency] = 0.0
            totals[currency] += account.balance

        return totals

    def get_account_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of all connected accounts."""
        accounts = self.get_accounts(user_id)
        connections = self.get_connections(user_id)

        # Group by type
        by_type: Dict[str, List[BankAccount]] = {}
        for acc in accounts:
            type_name = acc.account_type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(acc)

        # Group by bank
        by_bank: Dict[str, List[BankAccount]] = {}
        for acc in accounts:
            bank_name = acc.institution_name
            if bank_name not in by_bank:
                by_bank[bank_name] = []
            by_bank[bank_name].append(acc)

        return {
            "total_accounts": len(accounts),
            "connected_banks": len([c for c in connections if c.status == BankConnectionStatus.CONNECTED]),
            "total_balance": self.get_total_balance(user_id),
            "by_account_type": {
                type_name: {
                    "count": len(accs),
                    "total_balance": sum(a.balance for a in accs)
                }
                for type_name, accs in by_type.items()
            },
            "by_bank": {
                bank_name: {
                    "count": len(accs),
                    "total_balance": sum(a.balance for a in accs)
                }
                for bank_name, accs in by_bank.items()
            }
        }

    def get_recent_transactions(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[BankTransaction]:
        """Get recent transactions across all accounts."""
        all_transactions = []

        for account in self.get_accounts(user_id):
            transactions = self.get_transactions(account.id, limit=50)
            all_transactions.extend(transactions)

        # Sort by date descending
        all_transactions.sort(key=lambda t: t.date, reverse=True)

        return all_transactions[:limit]

    def get_spending_by_category(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """Get spending breakdown by category."""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        spending: Dict[str, float] = {}

        for account in self.get_accounts(user_id):
            transactions = self.get_transactions(
                account.id,
                start_date=start_date,
                end_date=end_date
            )

            for tx in transactions:
                if tx.amount < 0:  # Only spending (debits)
                    category = tx.category.value
                    if category not in spending:
                        spending[category] = 0.0
                    spending[category] += abs(tx.amount)

        return spending


# ==============================================================================
# SINGLETON INSTANCE
# ==============================================================================

canadian_banking_service = CanadianBankingService()


# ==============================================================================
# TEST
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CHE-NU Canadian Banking Service V72 - Test")
    print("=" * 60)

    service = canadian_banking_service
    user_id = "test-user-123"

    # Test 1: List supported banks
    print("\n1. Supported Canadian Banks:")
    banks = service.get_supported_banks()
    for bank in banks:
        print(f"   {bank['icon']} {bank['name']} ({bank['name_fr']})")

    # Test 2: Initiate connection
    print("\n2. Initiate Desjardins connection...")
    iframe_url, state = service.initiate_connection(user_id, CanadianBank.DESJARDINS)
    print(f"   URL: {iframe_url[:80]}...")
    print(f"   State: {state}")

    # Test 3: Complete connection (mock)
    print("\n3. Complete connection (mock)...")
    connection = service.complete_connection(
        state=state,
        login_id=f"login_{secrets.token_hex(8)}",
        institution="desjardins"
    )
    print(f"   Connection ID: {connection.id}")
    print(f"   Status: {connection.status.value}")
    print(f"   Accounts: {len(connection.accounts)}")

    # Test 4: Get accounts
    print("\n4. Get accounts:")
    accounts = service.get_accounts(user_id)
    for acc in accounts:
        print(f"   {acc.account_name}: ${acc.balance:,.2f} {acc.currency}")

    # Test 5: Get transactions
    print("\n5. Get recent transactions:")
    if accounts:
        transactions = service.get_transactions(accounts[0].id, limit=5)
        for tx in transactions:
            sign = "+" if tx.amount > 0 else ""
            print(f"   {tx.date.strftime('%Y-%m-%d')} | {sign}${tx.amount:,.2f} | {tx.description[:30]}")

    # Test 6: Account summary
    print("\n6. Account Summary:")
    summary = service.get_account_summary(user_id)
    print(f"   Total accounts: {summary['total_accounts']}")
    print(f"   Connected banks: {summary['connected_banks']}")
    print(f"   Total balance: {summary['total_balance']}")

    # Test 7: Spending by category
    print("\n7. Spending by Category (30 days):")
    spending = service.get_spending_by_category(user_id)
    for category, amount in spending.items():
        print(f"   {category}: ${amount:,.2f}")

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
