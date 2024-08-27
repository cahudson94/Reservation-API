"""."""

from uuid import UUID
from datetime import datetime

import strawberry
from pydantic import Field
from typing import Optional


@strawberry.type
class Appointment:
    """."""

    id: UUID = ""
    time: str = ""
    created_datetime: Optional[str] = ""
    provider_id: Optional[UUID] = ""
    client_id: Optional[UUID] = ""
    schedule_id: Optional[UUID] = ""
    status: Optional[str] = ""
    reserve_time: Optional[str] = ""


@strawberry.type
class AppointmentNotAvailable:
    """."""

    message: str = "Selected appointment is not currently available"


@strawberry.type
class AppointmentNotFound:
    """."""

    message: str = "Couldn't find appointment with the supplied id"


@strawberry.type
class AppointmentDeleted:
    """."""

    message: str = "appointment deleted and related appointments"
