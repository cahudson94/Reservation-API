"""."""

from uuid import UUID

from pydantic import Field
from typing import Optional, List
import strawberry

from api.scalars.schedule_scalar import Schedule


@strawberry.type
class Provider:
    """."""

    id: UUID = ""
    name: Optional[str] = ""
    schedules: Optional[List[Schedule]] = Field(default_factory=list)


@strawberry.type
class AddProvider:
    """."""

    id: UUID = ""
    name: Optional[str] = ""


@strawberry.type
class ProviderExists:
    """."""

    message: str = "provider with this name already exists"


@strawberry.type
class ProviderNotFound:
    """."""

    message: str = "Couldn't find provider with the supplied id"


@strawberry.type
class ProviderIdMissing:
    """."""

    message: str = "Please supply provider id"


@strawberry.type
class ProviderDeleted:
    """."""

    message: str = "provider deleted"
