"""
CHE·NU™ V75 - Meeting Models
Complete meeting system with notes, tasks, and participants.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.dataspace import DataSpace
    from models.identity import Identity
    from models.user import User
    from models.agent import Agent


class MeetingType(str, Enum):
    """Meeting types."""
    STANDUP = "standup"
    PLANNING = "planning"
    REVIEW = "review"
    BRAINSTORM = "brainstorm"
    DECISION = "decision"
    WORKSHOP = "workshop"
    PRESENTATION = "presentation"
    INTERVIEW = "interview"


class MeetingStatus(str, Enum):
    """Meeting status."""
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RSVPStatus(str, Enum):
    """RSVP status."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    TENTATIVE = "tentative"


class ParticipantRole(str, Enum):
    """Participant role."""
    ORGANIZER = "organizer"
    PARTICIPANT = "participant"
    OBSERVER = "observer"
    PRESENTER = "presenter"


class NoteType(str, Enum):
    """Note types."""
    GENERAL = "general"
    DECISION = "decision"
    ACTION = "action"
    QUESTION = "question"
    IDEA = "idea"


class TaskStatus(str, Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Meeting(Base):
    """
    Meeting model.
    
    Supports:
    - Multiple meeting types
    - XR/VR meetings
    - Agenda management
    - Integration with DataSpaces
    """
    
    __tablename__ = "meetings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    dataspace_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="CASCADE"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    meeting_type = Column(String(50), nullable=False)
    
    # Scheduling
    scheduled_start = Column(DateTime(timezone=True))
    scheduled_end = Column(DateTime(timezone=True))
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))
    
    status = Column(String(20), default=MeetingStatus.SCHEDULED.value)
    
    # Location
    location = Column(String(255))
    is_xr_meeting = Column(Boolean, default=False)
    xr_room_id = Column(UUID(as_uuid=True))
    
    # Agenda
    agenda = Column(JSON, default=list)
    
    # Metadata
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    dataspace = relationship("DataSpace", back_populates="meetings")
    participants = relationship("MeetingParticipant", back_populates="meeting", cascade="all, delete-orphan")
    notes = relationship("MeetingNote", back_populates="meeting", cascade="all, delete-orphan")
    tasks = relationship("MeetingTask", back_populates="meeting", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Meeting {self.title}>"
    
    @property
    def duration_minutes(self) -> Optional[int]:
        """Calculate meeting duration."""
        if self.actual_start and self.actual_end:
            delta = self.actual_end - self.actual_start
            return int(delta.total_seconds() / 60)
        elif self.scheduled_start and self.scheduled_end:
            delta = self.scheduled_end - self.scheduled_start
            return int(delta.total_seconds() / 60)
        return None
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "dataspace_id": str(self.dataspace_id),
            "title": self.title,
            "description": self.description,
            "meeting_type": self.meeting_type,
            "scheduled_start": self.scheduled_start.isoformat() if self.scheduled_start else None,
            "scheduled_end": self.scheduled_end.isoformat() if self.scheduled_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "status": self.status,
            "location": self.location,
            "is_xr_meeting": self.is_xr_meeting,
            "agenda": self.agenda,
            "duration_minutes": self.duration_minutes,
            "participants_count": len(self.participants) if self.participants else 0,
            "notes_count": len(self.notes) if self.notes else 0,
            "tasks_count": len(self.tasks) if self.tasks else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class MeetingParticipant(Base):
    """Meeting participant."""
    
    __tablename__ = "meeting_participants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    role = Column(String(50), default=ParticipantRole.PARTICIPANT.value)
    rsvp_status = Column(String(20), default=RSVPStatus.PENDING.value)
    
    joined_at = Column(DateTime(timezone=True))
    left_at = Column(DateTime(timezone=True))
    
    # Relationships
    meeting = relationship("Meeting", back_populates="participants")
    user = relationship("User")
    
    def __repr__(self):
        return f"<MeetingParticipant {self.user_id} in {self.meeting_id}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "meeting_id": str(self.meeting_id),
            "user_id": str(self.user_id) if self.user_id else None,
            "role": self.role,
            "rsvp_status": self.rsvp_status,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "left_at": self.left_at.isoformat() if self.left_at else None,
        }


class MeetingNote(Base):
    """Meeting note - can be created by user or agent."""
    
    __tablename__ = "meeting_notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    
    note_type = Column(String(50), default=NoteType.GENERAL.value)
    content = Column(Text, nullable=False)
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="notes")
    
    def __repr__(self):
        return f"<MeetingNote {self.note_type}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "meeting_id": str(self.meeting_id),
            "note_type": self.note_type,
            "content": self.content,
            "created_by": str(self.created_by) if self.created_by else None,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": self.metadata,
        }


class MeetingTask(Base):
    """
    Task created from meeting.
    
    GOUVERNANCE: Tasks require human assignment and approval.
    """
    
    __tablename__ = "meeting_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    due_date = Column(Date)
    
    status = Column(String(20), default=TaskStatus.PENDING.value)
    priority = Column(String(20), default=TaskPriority.MEDIUM.value)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="tasks")
    assignee = relationship("User")
    
    def __repr__(self):
        return f"<MeetingTask {self.title}>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status != TaskStatus.COMPLETED.value:
            return date.today() > self.due_date
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "meeting_id": str(self.meeting_id),
            "title": self.title,
            "description": self.description,
            "assignee_id": str(self.assignee_id) if self.assignee_id else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "priority": self.priority,
            "is_overdue": self.is_overdue,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
