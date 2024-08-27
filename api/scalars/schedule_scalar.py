"""."""
from uuid import UUID
from datetime import datetime

from pydantic import Field
from typing import Optional, List
import strawberry

from api.scalars.appointment_scalar import Appointment

@strawberry.type
class Schedule:
    """."""

    id: UUID = ""
    start: datetime = Field(default_factory=datetime.now())
    end: datetime = Field(default_factory=datetime.now())
    created_datetime : Optional[datetime] = Field(default_factory=datetime.now())
    provider_id: Optional[UUID] = Field(default_factory="", description="Provider id")
    appointments: Optional[List[Appointment]] = Field(default_factory=list)

@strawberry.type
class ScheduleNotFound:
    """."""

    message: str = "Couldn't find schedule with the supplied id"

@strawberry.type
class ScheduleDeleted:
    """."""

    message: str = "Schedule deleted and related appointments"
