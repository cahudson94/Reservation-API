"""."""

from uuid import UUID
from datetime import datetime

from pydantic import Field
from typing import Optional, List
import strawberry

from api.scalars.appointment_scalar import Appointment


@strawberry.type
class Client:
    """."""

    id: UUID = ""
    name: Optional[str] = ""
    appointments: Optional[List[Appointment]] = Field(default_factory=list)


@strawberry.type
class AddClient:
    """."""

    id: UUID = ""
    name: Optional[str] = ""


@strawberry.type
class ClientExists:
    """."""

    message: str = "client with this name already exists"


@strawberry.type
class ClientNotFound:
    """."""

    message: str = "Couldn't find client with the supplied id"


@strawberry.type
class ClientIdMissing:
    """."""

    message: str = "Please supply client id"


@strawberry.type
class ClientDeleted:
    """."""

    message: str = "client deleted"
