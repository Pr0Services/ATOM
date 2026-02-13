"""
Waitlist Service

Business logic for waitlist management:
- Email validation and normalization
- Deduplication
- Source tracking
- Consent and timestamp tracking
- Statistics computation
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from uuid import uuid4
import re
import logging
from dataclasses import dataclass, field

from app.schemas.waitlist_schemas import (
    WaitlistSource,
    WaitlistStatus,
    WaitlistSubmitRequest,
    WaitlistEntry,
    WaitlistResponse,
    WaitlistCheckResponse,
    WaitlistStats,
    WaitlistEntryCreate,
    WaitlistEntryUpdate,
)

logger = logging.getLogger(__name__)


# =============================================================================
# IN-MEMORY REPOSITORY (Replace with DB in production)
# =============================================================================

@dataclass
class WaitlistRepository:
    """
    In-memory waitlist repository.

    In production, replace with SQLAlchemy/database implementation.
    """

    _entries: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _email_index: Dict[str, str] = field(default_factory=dict)  # email -> entry_id
    _position_counter: int = 0

    def add(self, entry: Dict[str, Any]) -> None:
        """Add entry to repository."""
        self._entries[entry["id"]] = entry
        self._email_index[entry["email"]] = entry["id"]

    def get_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get entry by ID."""
        return self._entries.get(entry_id)

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get entry by email."""
        entry_id = self._email_index.get(email.lower())
        if entry_id:
            return self._entries.get(entry_id)
        return None

    def email_exists(self, email: str) -> bool:
        """Check if email exists."""
        return email.lower() in self._email_index

    def update(self, entry_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update entry."""
        if entry_id in self._entries:
            self._entries[entry_id].update(updates)
            self._entries[entry_id]["updated_at"] = datetime.now(timezone.utc)
            return self._entries[entry_id]
        return None

    def delete(self, entry_id: str) -> bool:
        """Delete entry."""
        if entry_id in self._entries:
            email = self._entries[entry_id]["email"]
            del self._entries[entry_id]
            if email in self._email_index:
                del self._email_index[email]
            return True
        return False

    def get_next_position(self) -> int:
        """Get next queue position."""
        self._position_counter += 1
        return self._position_counter

    def count_all(self) -> int:
        """Count all entries."""
        return len(self._entries)

    def count_by_status(self, status: WaitlistStatus) -> int:
        """Count entries by status."""
        return sum(1 for e in self._entries.values() if e.get("status") == status)

    def count_by_source(self, source: WaitlistSource) -> int:
        """Count entries by source."""
        return sum(1 for e in self._entries.values() if e.get("source") == source)

    def count_since(self, since: datetime) -> int:
        """Count entries since datetime."""
        return sum(
            1 for e in self._entries.values()
            if e.get("created_at") and e["created_at"] >= since
        )

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent entries."""
        sorted_entries = sorted(
            self._entries.values(),
            key=lambda x: x.get("created_at", datetime.min),
            reverse=True
        )
        return sorted_entries[:limit]

    def get_pending_oldest(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get oldest pending entries (for invitations)."""
        pending = [
            e for e in self._entries.values()
            if e.get("status") == WaitlistStatus.PENDING
        ]
        sorted_entries = sorted(
            pending,
            key=lambda x: x.get("created_at", datetime.max)
        )
        return sorted_entries[:limit]


# Global repository instance
_repository = WaitlistRepository()


# =============================================================================
# EMAIL VALIDATION
# =============================================================================

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email address.

    Returns:
        (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    email = email.lower().strip()

    # Basic format check
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    # Check for disposable email domains (basic list)
    disposable_domains = {
        "tempmail.com", "throwaway.email", "mailinator.com",
        "guerrillamail.com", "10minutemail.com", "temp-mail.org",
        "fakeinbox.com", "trashmail.com", "yopmail.com"
    }

    domain = email.split("@")[1]
    if domain in disposable_domains:
        return False, "Disposable email addresses are not allowed"

    # Length check
    if len(email) > 254:
        return False, "Email address is too long"

    return True, ""


def normalize_email(email: str) -> str:
    """Normalize email address."""
    return email.lower().strip()


# =============================================================================
# WAITLIST SERVICE
# =============================================================================

class WaitlistService:
    """
    Waitlist management service.

    Handles:
    - Email submission with validation
    - Deduplication
    - Source and campaign tracking
    - Consent management
    - Statistics computation
    """

    def __init__(self, repository: WaitlistRepository = None):
        self.repository = repository or _repository

    # =========================================================================
    # SUBMISSION
    # =========================================================================

    async def submit(self, request: WaitlistSubmitRequest) -> WaitlistResponse:
        """
        Submit email to waitlist.

        Args:
            request: Submission request with email and metadata

        Returns:
            WaitlistResponse with status and position
        """
        email = normalize_email(request.email)

        # Validate email
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            logger.warning(f"Invalid email submission: {email} - {error_msg}")
            return WaitlistResponse(
                success=False,
                message=error_msg,
                already_exists=False
            )

        # Check consent
        if not request.consent:
            return WaitlistResponse(
                success=False,
                message="Consent is required to join the waitlist",
                already_exists=False
            )

        # Check for duplicate
        existing = self.repository.get_by_email(email)
        if existing:
            logger.info(f"Duplicate waitlist submission: {email}")
            return WaitlistResponse(
                success=True,
                message="You're already on the waitlist!",
                position=existing.get("position"),
                already_exists=True,
                entry_id=existing.get("id")
            )

        # Create entry
        now = datetime.now(timezone.utc)
        entry_id = str(uuid4())
        position = self.repository.get_next_position()

        entry = {
            "id": entry_id,
            "email": email,
            "source": request.source,
            "campaign": request.campaign,
            "referrer": request.referrer,
            "status": WaitlistStatus.PENDING,
            "consent": request.consent,
            "consent_timestamp": now,
            "position": position,
            "created_at": now,
            "updated_at": now,
            "invited_at": None,
            "registered_at": None,
            "metadata": request.metadata
        }

        self.repository.add(entry)

        logger.info(
            f"Waitlist signup: {email} | source={request.source} | "
            f"campaign={request.campaign} | position={position}"
        )

        return WaitlistResponse(
            success=True,
            message=f"Welcome to the waitlist! You're #{position} in line.",
            position=position,
            already_exists=False,
            entry_id=entry_id
        )

    # =========================================================================
    # CHECK
    # =========================================================================

    async def check_email(self, email: str) -> WaitlistCheckResponse:
        """
        Check if email exists on waitlist.

        Args:
            email: Email to check

        Returns:
            WaitlistCheckResponse with status
        """
        email = normalize_email(email)
        entry = self.repository.get_by_email(email)

        if not entry:
            return WaitlistCheckResponse(
                exists=False,
                status=None,
                position=None,
                message="Email not found on waitlist"
            )

        status = entry.get("status", WaitlistStatus.PENDING)
        position = entry.get("position") if status == WaitlistStatus.PENDING else None

        status_messages = {
            WaitlistStatus.PENDING: f"You're #{position} on the waitlist",
            WaitlistStatus.INVITED: "Check your email for your invitation!",
            WaitlistStatus.REGISTERED: "You've already registered",
            WaitlistStatus.DECLINED: "You previously declined the invitation"
        }

        return WaitlistCheckResponse(
            exists=True,
            status=status,
            position=position,
            message=status_messages.get(status, "Email is on the waitlist")
        )

    # =========================================================================
    # STATISTICS (Admin)
    # =========================================================================

    async def get_stats(self) -> WaitlistStats:
        """
        Get waitlist statistics.

        Returns:
            WaitlistStats with comprehensive metrics
        """
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = today_start.replace(day=1)

        # Count by status
        total = self.repository.count_all()
        pending = self.repository.count_by_status(WaitlistStatus.PENDING)
        invited = self.repository.count_by_status(WaitlistStatus.INVITED)
        registered = self.repository.count_by_status(WaitlistStatus.REGISTERED)
        declined = self.repository.count_by_status(WaitlistStatus.DECLINED)

        # Count by source
        by_source = {}
        for source in WaitlistSource:
            by_source[source.value] = self.repository.count_by_source(source)

        # Time-based counts
        signups_today = self.repository.count_since(today_start)
        signups_this_week = self.repository.count_since(week_start)
        signups_this_month = self.repository.count_since(month_start)

        # Conversion rate
        invite_to_register_rate = 0.0
        if invited + registered > 0:
            invite_to_register_rate = (registered / (invited + registered)) * 100

        # Recent signups
        recent_entries = self.repository.get_recent(limit=10)
        recent_signups = [
            WaitlistEntry(
                id=e["id"],
                email=e["email"],
                source=e["source"],
                campaign=e.get("campaign"),
                referrer=e.get("referrer"),
                status=e.get("status", WaitlistStatus.PENDING),
                consent=e["consent"],
                consent_timestamp=e["consent_timestamp"],
                position=e["position"],
                created_at=e["created_at"],
                updated_at=e["updated_at"],
                invited_at=e.get("invited_at"),
                registered_at=e.get("registered_at"),
                metadata=e.get("metadata")
            )
            for e in recent_entries
        ]

        return WaitlistStats(
            total_entries=total,
            pending_count=pending,
            invited_count=invited,
            registered_count=registered,
            declined_count=declined,
            by_source=by_source,
            signups_today=signups_today,
            signups_this_week=signups_this_week,
            signups_this_month=signups_this_month,
            invite_to_register_rate=round(invite_to_register_rate, 2),
            recent_signups=recent_signups,
            timestamp=now
        )

    # =========================================================================
    # ADMIN OPERATIONS
    # =========================================================================

    async def invite_batch(
        self,
        count: int,
        source_filter: Optional[WaitlistSource] = None
    ) -> List[str]:
        """
        Mark batch of entries as invited.

        Args:
            count: Number to invite
            source_filter: Only invite from specific source

        Returns:
            List of invited entry IDs
        """
        pending = self.repository.get_pending_oldest(limit=count * 2)

        if source_filter:
            pending = [e for e in pending if e.get("source") == source_filter]

        invited_ids = []
        now = datetime.now(timezone.utc)

        for entry in pending[:count]:
            self.repository.update(entry["id"], {
                "status": WaitlistStatus.INVITED,
                "invited_at": now
            })
            invited_ids.append(entry["id"])
            logger.info(f"Waitlist invitation sent: {entry['email']}")

        return invited_ids

    async def mark_registered(self, email: str) -> bool:
        """
        Mark entry as registered.

        Args:
            email: Email that registered

        Returns:
            True if updated, False if not found
        """
        email = normalize_email(email)
        entry = self.repository.get_by_email(email)

        if not entry:
            return False

        self.repository.update(entry["id"], {
            "status": WaitlistStatus.REGISTERED,
            "registered_at": datetime.now(timezone.utc)
        })

        logger.info(f"Waitlist user registered: {email}")
        return True

    async def get_entry(self, entry_id: str) -> Optional[WaitlistEntry]:
        """Get single entry by ID."""
        entry = self.repository.get_by_id(entry_id)
        if not entry:
            return None

        return WaitlistEntry(
            id=entry["id"],
            email=entry["email"],
            source=entry["source"],
            campaign=entry.get("campaign"),
            referrer=entry.get("referrer"),
            status=entry.get("status", WaitlistStatus.PENDING),
            consent=entry["consent"],
            consent_timestamp=entry["consent_timestamp"],
            position=entry["position"],
            created_at=entry["created_at"],
            updated_at=entry["updated_at"],
            invited_at=entry.get("invited_at"),
            registered_at=entry.get("registered_at"),
            metadata=entry.get("metadata")
        )

    async def delete_entry(self, entry_id: str) -> bool:
        """Delete entry from waitlist."""
        return self.repository.delete(entry_id)


# =============================================================================
# SERVICE FACTORY
# =============================================================================

def get_waitlist_service() -> WaitlistService:
    """Factory function for WaitlistService."""
    return WaitlistService()
