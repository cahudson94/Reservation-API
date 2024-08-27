"""."""
import strawberry

from api.scalars.schedule_scalar import Schedule, ScheduleDeleted, ScheduleNotFound
from api.scalars.provider_scalar import ProviderNotFound


AddScheduleResponse = strawberry.union("AddScheduleResponse", (Schedule, ProviderNotFound))
UpdateScheduleResponse = strawberry.union("UpdateScheduleResponse", (Schedule, ScheduleNotFound))
DeleteScheduleResponse = strawberry.union("DeleteScheduleResponse", (ScheduleDeleted, ScheduleNotFound))
