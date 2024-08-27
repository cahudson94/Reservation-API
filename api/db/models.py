"""."""

from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import Column, String, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Optional

Base = declarative_base()


class Client(Base):
    """."""

    __tablename__ = "client"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created_datetime: DateTime = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    name: Optional[str] = Column(String, nullable=True)

    appointments = relationship(
        "Appointment", cascade="all, delete", passive_deletes=True
    )

    def __dict__(self):
        """."""
        return {
            "id": self.id,
            "name": self.name,
            "created_datetime": self.created_datetime,
            "appointments": self.appointments,
        }


class Provider(Base):
    """."""

    __tablename__ = "provider"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created_datetime: DateTime = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    name: Optional[str] = Column(String, nullable=True)

    schedules = relationship("Schedule", cascade="all, delete", passive_deletes=True)
    appointments = relationship(
        "Appointment", cascade="all, delete", passive_deletes=True
    )

    def __dict__(self):
        """."""
        return {
            "id": self.id,
            "name": self.name,
            "created_datetime": self.created_datetime,
            "schedules": self.schedules,
            "appointments": self.appointments,
        }


class Schedule(Base):
    """."""

    __tablename__ = "schedule"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    provider_id: Optional[UUID] = Column(
        UUID(as_uuid=True), ForeignKey(Provider.id, ondelete="CASCADE"), nullable=False
    )
    created_datetime: DateTime = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    start: DateTime = Column(DateTime, nullable=False)
    end: DateTime = Column(DateTime, nullable=False)

    appointments = relationship(
        "Appointment", cascade="all, delete", passive_deletes=True
    )

    def __dict__(self):
        """."""
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "start": self.start,
            "end": self.end,
            "created_datetime": self.created_datetime,
            "appointments": self.appointments,
        }


class Appointment(Base):
    """."""

    __tablename__ = "appointment"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    client_id: Optional[UUID] = Column(
        UUID(as_uuid=True), ForeignKey(Client.id, ondelete="CASCADE"), nullable=True
    )
    provider_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey(Provider.id, ondelete="CASCADE"), nullable=False
    )
    schedule_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey(Schedule.id, ondelete="CASCADE"), nullable=False
    )
    created_datetime: DateTime = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    time: DateTime = Column(DateTime, nullable=False)
    reserve_time: DateTime = Column(DateTime, nullable=False, default=datetime.min)
    status: String = Column(String, nullable=False, default="avail")
    __tableargs__ = (CheckConstraint(status.in_(["avail", "res", "conf", "unsched"])),)

    def __dict__(self):
        """."""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "provider_id": self.provider_id,
            "schedule_id": self.schedule_id,
            "time": self.time,
            "created_datetime": self.created_datetime,
        }
