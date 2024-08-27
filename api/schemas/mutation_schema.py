"""."""
from uuid import UUID
from datetime import datetime

import strawberry

from api.helpers import date_range
from api.resolvers.appointment_resolver import add_appointment, update_appointment, delete_appointment
from api.fragments.appointment_fragments import (
    AddAppointmentResponse, UpdateAppointmentResponse, DeleteAppointmentResponse
)
from api.resolvers.client_resolver import add_client, delete_client
from api.fragments.client_fragments import AddClientResponse, DeleteClientResponse
from api.resolvers.provider_resolver import add_provider, delete_provider
from api.fragments.provider_fragments import AddProviderResponse, DeleteProviderResponse
from api.resolvers.schedule_resolver import add_schedule, delete_schedule, update_schedule
from api.fragments.schedule_fragments import AddScheduleResponse, DeleteScheduleResponse, UpdateScheduleResponse


@strawberry.type
class Mutation:
    """GraphQL Mutations."""

    @strawberry.mutation
    async def add_appointment(self, provider_id: UUID, schedule_id: UUID, time: datetime) -> AddAppointmentResponse:
        """Add a appointment."""
        add_appointment_resp = await add_appointment(provider_id, schedule_id, time)
        return add_appointment_resp

    @strawberry.mutation
    async def update_appointment(self, appointment_id: UUID, client_id: UUID = None, status: str = "") -> UpdateAppointmentResponse:
        """Update Appointment."""
        update_appointment_resp = await update_appointment(appointment_id, client_id, status)
        return update_appointment_resp

    @strawberry.mutation
    async def delete_appointment(self, appointment_id: UUID) -> DeleteAppointmentResponse:
        """Delete Appointment."""
        delete_appointment_resp = await delete_appointment(appointment_id)
        return delete_appointment_resp

    @strawberry.mutation
    async def add_client(self, name: str) -> AddClientResponse:
        """Add client."""
        add_client_resp = await add_client(name)
        return add_client_resp

    @strawberry.mutation
    async def delete_client(self, client_id: UUID) -> DeleteClientResponse:
        """Delete client."""
        delete_client_resp = await delete_client(client_id)
        return delete_client_resp

    @strawberry.mutation
    async def add_provider(self, name: str) -> AddProviderResponse:
        """Add provider."""
        add_provider_resp = await add_provider(name)
        return add_provider_resp

    @strawberry.mutation
    async def delete_provider(self, provider_id: UUID) -> DeleteProviderResponse:
        """Delete provider."""
        delete_provider_resp = await delete_provider(provider_id)
        return delete_provider_resp

    @strawberry.mutation
    async def add_schedule(self, provider_id: UUID, start: datetime, end: datetime) -> AddScheduleResponse:
        """Add a Schedule."""
        add_schedule_resp = await add_schedule(provider_id, start, end)
        for apt_time in date_range(start, end):
            await add_appointment(provider_id, add_schedule_resp.id, apt_time)
        return add_schedule_resp

    @strawberry.mutation
    async def update_schedule(self, schedule_id: UUID, start: datetime, end: datetime) -> UpdateScheduleResponse:
        """Update Schedule, and the releated appointments."""
        update_schedule_resp = await update_schedule(schedule_id, start, end)
        for apt_time in date_range(start, end):
            await add_appointment(provider_id, schedule_id, apt_time)
        return update_schedule_resp

    @strawberry.mutation
    async def delete_schedule(self, schedule_id: UUID) -> DeleteScheduleResponse:
        """Delete Schedule, and the releated appointments."""
        delete_schedule_resp = await delete_schedule(schedule_id)
        return delete_schedule_resp
