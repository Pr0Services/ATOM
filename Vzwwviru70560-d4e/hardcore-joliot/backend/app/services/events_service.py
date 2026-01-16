"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V77 — Events Service
═══════════════════════════════════════════════════════════════════════════════

Version: 77.0
Purpose: Backend service for community event management

R&D Rules Enforced:
- Rule #1: Checkpoint required for event creation/cancellation
- Rule #5: CHRONOLOGICAL ONLY - No popularity-based event ranking
- Rule #6: Full traceability on all operations
═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import logging

logger = logging.getLogger("chenu.events")


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class EventType(str, Enum):
    MEETUP = "meetup"
    WORKSHOP = "workshop"
    WEBINAR = "webinar"
    FUNDRAISER = "fundraiser"
    VOLUNTEER = "volunteer"
    SOCIAL = "social"
    CONFERENCE = "conference"
    OTHER = "other"


class RSVPStatus(str, Enum):
    ATTENDING = "attending"
    NOT_ATTENDING = "not_attending"
    MAYBE = "maybe"
    WAITLIST = "waitlist"


class RecurrencePattern(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EventDetails:
    """Detailed event information."""
    id: UUID
    title: str
    description: str
    event_type: EventType
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    is_online: bool = False
    meeting_url: Optional[str] = None
    max_attendees: Optional[int] = None
    
    # Recurrence
    recurrence: RecurrencePattern = RecurrencePattern.NONE
    recurrence_end: Optional[date] = None
    
    # Approval status
    is_approved: bool = False
    requires_approval: bool = True
    
    # R&D Rule #6: Traceability
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: UUID = field(default_factory=uuid4)
    approved_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None


@dataclass
class RSVP:
    """Event RSVP record."""
    id: UUID
    event_id: UUID
    user_id: UUID
    status: RSVPStatus
    guests: int = 0
    notes: Optional[str] = None
    
    # R&D Rule #6: Traceability
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: UUID = field(default_factory=uuid4)
    updated_at: Optional[datetime] = None


@dataclass
class EventReminder:
    """Event reminder."""
    id: UUID
    event_id: UUID
    user_id: UUID
    remind_at: datetime
    sent: bool = False
    sent_at: Optional[datetime] = None
    
    # R&D Rule #6: Traceability
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EventSummary:
    """Event summary for listings."""
    id: UUID
    title: str
    event_type: EventType
    start_datetime: datetime
    location: Optional[str]
    is_online: bool
    attendee_count: int
    max_attendees: Optional[int]
    is_full: bool
    
    # R&D Rule #6: Traceability
    created_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# EVENTS SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class EventsService:
    """
    Service for managing community events.
    
    ⚠️ R&D COMPLIANCE:
    - All events require human approval before publishing
    - No popularity-based ranking of events
    - All listings in chronological order
    """
    
    def __init__(self):
        self._events: Dict[UUID, EventDetails] = {}
        self._rsvps: Dict[UUID, List[RSVP]] = {}  # event_id -> list of RSVPs
        self._reminders: Dict[UUID, List[EventReminder]] = {}
        
    # ═══════════════════════════════════════════════════════════════════════════
    # EVENT CRUD
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_event(
        self,
        title: str,
        description: str,
        event_type: EventType,
        start_datetime: datetime,
        end_datetime: datetime,
        user_id: UUID,
        location: Optional[str] = None,
        is_online: bool = False,
        meeting_url: Optional[str] = None,
        max_attendees: Optional[int] = None,
    ) -> EventDetails:
        """
        Create a new event.
        
        Note: Events are created with is_approved=False.
        Approval must be granted via checkpoint system.
        """
        event = EventDetails(
            id=uuid4(),
            title=title,
            description=description,
            event_type=event_type,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            is_online=is_online,
            meeting_url=meeting_url,
            max_attendees=max_attendees,
            is_approved=False,
            requires_approval=True,
            created_by=user_id,
        )
        
        self._events[event.id] = event
        self._rsvps[event.id] = []
        
        logger.info(f"Created event {event.id}: {title} (pending approval)")
        
        return event
    
    async def get_event(self, event_id: UUID) -> Optional[EventDetails]:
        """Get event by ID."""
        return self._events.get(event_id)
    
    async def approve_event(
        self,
        event_id: UUID,
        approver_id: UUID,
    ) -> Optional[EventDetails]:
        """
        Approve an event for publication.
        
        This should only be called after checkpoint approval.
        """
        event = self._events.get(event_id)
        if not event:
            return None
        
        event.is_approved = True
        event.approved_at = datetime.utcnow()
        event.approved_by = approver_id
        
        logger.info(f"Approved event {event_id} by user {approver_id}")
        
        return event
    
    async def cancel_event(self, event_id: UUID) -> bool:
        """Cancel an event."""
        if event_id not in self._events:
            return False
        
        del self._events[event_id]
        self._rsvps.pop(event_id, None)
        self._reminders.pop(event_id, None)
        
        logger.info(f"Cancelled event {event_id}")
        
        return True
    
    async def list_events(
        self,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        event_type: Optional[EventType] = None,
        approved_only: bool = True,
        limit: int = 20,
    ) -> List[EventSummary]:
        """
        List events.
        
        ⚠️ R&D Rule #5: Events ordered by start_datetime (chronological).
        NO popularity ranking.
        """
        events = list(self._events.values())
        
        # Filter by approval status
        if approved_only:
            events = [e for e in events if e.is_approved]
        
        # Filter by date range
        if from_date:
            events = [e for e in events if e.start_datetime.date() >= from_date]
        if to_date:
            events = [e for e in events if e.start_datetime.date() <= to_date]
        
        # Filter by type
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # R&D Rule #5: CHRONOLOGICAL ORDER
        events.sort(key=lambda x: x.start_datetime)
        
        # Convert to summaries
        summaries = []
        for e in events[:limit]:
            rsvps = self._rsvps.get(e.id, [])
            attendee_count = len([r for r in rsvps if r.status == RSVPStatus.ATTENDING])
            
            summaries.append(EventSummary(
                id=e.id,
                title=e.title,
                event_type=e.event_type,
                start_datetime=e.start_datetime,
                location=e.location,
                is_online=e.is_online,
                attendee_count=attendee_count,
                max_attendees=e.max_attendees,
                is_full=e.max_attendees is not None and attendee_count >= e.max_attendees,
                created_at=e.created_at,
            ))
        
        return summaries
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RSVP MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def rsvp(
        self,
        event_id: UUID,
        user_id: UUID,
        status: RSVPStatus,
        guests: int = 0,
        notes: Optional[str] = None,
    ) -> Optional[RSVP]:
        """
        RSVP to an event.
        
        Returns None if event not found or is full.
        """
        event = self._events.get(event_id)
        if not event:
            return None
        
        if not event.is_approved:
            return None
        
        rsvps = self._rsvps.get(event_id, [])
        
        # Check capacity
        if status == RSVPStatus.ATTENDING:
            current_attendees = len([r for r in rsvps if r.status == RSVPStatus.ATTENDING])
            if event.max_attendees and current_attendees >= event.max_attendees:
                # Add to waitlist instead
                status = RSVPStatus.WAITLIST
        
        # Update existing RSVP or create new
        existing = next((r for r in rsvps if r.user_id == user_id), None)
        
        if existing:
            existing.status = status
            existing.guests = guests
            existing.notes = notes
            existing.updated_at = datetime.utcnow()
            return existing
        
        rsvp = RSVP(
            id=uuid4(),
            event_id=event_id,
            user_id=user_id,
            status=status,
            guests=guests,
            notes=notes,
            created_by=user_id,
        )
        
        self._rsvps[event_id].append(rsvp)
        
        logger.info(f"RSVP {status.value} for event {event_id} by user {user_id}")
        
        return rsvp
    
    async def get_rsvps(
        self,
        event_id: UUID,
        status: Optional[RSVPStatus] = None,
    ) -> List[RSVP]:
        """Get RSVPs for an event."""
        rsvps = self._rsvps.get(event_id, [])
        
        if status:
            rsvps = [r for r in rsvps if r.status == status]
        
        # Chronological order
        rsvps.sort(key=lambda x: x.created_at)
        
        return rsvps
    
    async def get_attendee_count(self, event_id: UUID) -> int:
        """Get number of confirmed attendees."""
        rsvps = self._rsvps.get(event_id, [])
        return len([r for r in rsvps if r.status == RSVPStatus.ATTENDING])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # REMINDERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_reminder(
        self,
        event_id: UUID,
        user_id: UUID,
        remind_before_hours: int = 24,
    ) -> Optional[EventReminder]:
        """Create event reminder."""
        event = self._events.get(event_id)
        if not event:
            return None
        
        remind_at = event.start_datetime - timedelta(hours=remind_before_hours)
        
        reminder = EventReminder(
            id=uuid4(),
            event_id=event_id,
            user_id=user_id,
            remind_at=remind_at,
        )
        
        if event_id not in self._reminders:
            self._reminders[event_id] = []
        
        self._reminders[event_id].append(reminder)
        
        return reminder
    
    async def get_pending_reminders(self) -> List[EventReminder]:
        """Get reminders that need to be sent."""
        now = datetime.utcnow()
        pending = []
        
        for reminders in self._reminders.values():
            for r in reminders:
                if not r.sent and r.remind_at <= now:
                    pending.append(r)
        
        return pending
    
    async def mark_reminder_sent(self, reminder_id: UUID) -> bool:
        """Mark reminder as sent."""
        for reminders in self._reminders.values():
            for r in reminders:
                if r.id == reminder_id:
                    r.sent = True
                    r.sent_at = datetime.utcnow()
                    return True
        return False
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RECURRENCE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def generate_recurring_events(
        self,
        event_id: UUID,
        until: date,
    ) -> List[EventDetails]:
        """
        Generate recurring event instances.
        
        Note: Each generated instance requires separate approval.
        """
        event = self._events.get(event_id)
        if not event or event.recurrence == RecurrencePattern.NONE:
            return []
        
        generated = []
        current = event.start_datetime
        
        while current.date() <= until:
            # Calculate next occurrence
            if event.recurrence == RecurrencePattern.DAILY:
                current += timedelta(days=1)
            elif event.recurrence == RecurrencePattern.WEEKLY:
                current += timedelta(weeks=1)
            elif event.recurrence == RecurrencePattern.BIWEEKLY:
                current += timedelta(weeks=2)
            elif event.recurrence == RecurrencePattern.MONTHLY:
                # Simple approximation
                current += timedelta(days=30)
            
            if current.date() > until:
                break
            
            # Create new instance
            duration = event.end_datetime - event.start_datetime
            new_event = EventDetails(
                id=uuid4(),
                title=event.title,
                description=event.description,
                event_type=event.event_type,
                start_datetime=current,
                end_datetime=current + duration,
                location=event.location,
                is_online=event.is_online,
                meeting_url=event.meeting_url,
                max_attendees=event.max_attendees,
                recurrence=RecurrencePattern.NONE,  # Instances don't recur
                is_approved=False,  # Each instance needs approval
                requires_approval=True,
                created_by=event.created_by,
            )
            
            self._events[new_event.id] = new_event
            self._rsvps[new_event.id] = []
            generated.append(new_event)
        
        return generated


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

events_service = EventsService()


async def get_events_service() -> EventsService:
    """Dependency injection for events service."""
    return events_service
