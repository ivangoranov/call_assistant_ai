"""
Database models for AI Call Summarizer.

Tables:
- users
- calls
- transcripts
- summaries
- tasks
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class CallStatus(str, Enum):
    """Call lifecycle statuses."""

    RECORDING = "recording"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    calls: Mapped[list["Call"]] = relationship("Call", back_populates="user")


class Call(Base):
    """Call model - represents a VoIP call."""

    __tablename__ = "calls"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[CallStatus] = mapped_column(
        String(20), default=CallStatus.RECORDING, nullable=False
    )
    consent_given: Mapped[bool] = mapped_column(Boolean, default=True)
    audio_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="calls")
    transcript: Mapped[Optional["Transcript"]] = relationship(
        "Transcript", back_populates="call", uselist=False
    )
    summary: Mapped[Optional["Summary"]] = relationship(
        "Summary", back_populates="call", uselist=False
    )
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="call")


class Transcript(Base):
    """Transcript model - raw transcription of call audio."""

    __tablename__ = "transcripts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    call_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("calls.id"), unique=True, nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="bg", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    call: Mapped["Call"] = relationship("Call", back_populates="transcript")


class Summary(Base):
    """Summary model - AI-generated summary of the call."""

    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    call_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("calls.id"), unique=True, nullable=False
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    topics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    decisions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    dates: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    amounts: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    locations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    call: Mapped["Call"] = relationship("Call", back_populates="summary")


class Task(Base):
    """Task model - extracted tasks from the call."""

    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    call_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("calls.id"), nullable=False
    )
    task_text: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deadline: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    call: Mapped["Call"] = relationship("Call", back_populates="tasks")
