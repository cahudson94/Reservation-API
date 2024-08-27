"""."""

from uuid import UUID

from pydantic import typing
import strawberry
from strawberry.types import Info
from typing import Optional

from api.resolvers.appointment_resolver import get_appointment, get_appointments
from api.scalars.appointment_scalar import Appointment
from api.resolvers.client_resolver import get_client, get_clients
from api.scalars.client_scalar import Client
from api.resolvers.provider_resolver import get_provider, get_providers
from api.scalars.provider_scalar import Provider
from api.resolvers.schedule_resolver import get_schedule, get_schedules
from api.scalars.schedule_scalar import Schedule


@strawberry.type
class Query:
    """GraphQL Queries."""

    @strawberry.field
    async def appointments(
        self, info: Info, provider_id: Optional[UUID] = None
    ) -> typing.List[Appointment]:
        """Get all available appointments, optionally filtered to a single provider."""
        appointments_data_list = await get_appointments(info, provider_id)
        return appointments_data_list

    @strawberry.field
    async def appointment(self, info: Info, appointment_id: UUID) -> Appointment:
        """Get appointment by id"""
        appointment_dict = await get_appointment(appointment_id, info)
        return appointment_dict

    @strawberry.field
    async def clients(self, info: Info) -> typing.List[Client]:
        """Get all clients."""
        clients_data_list = await get_clients(info)
        return clients_data_list

    @strawberry.field
    async def client(self, info: Info, client_id: UUID) -> Client:
        """Get client by id."""
        client_dict = await get_client(client_id, info)
        return client_dict

    @strawberry.field
    async def providers(self, info: Info) -> typing.List[Provider]:
        """Get all providers."""
        providers_data_list = await get_providers(info)
        return providers_data_list

    @strawberry.field
    async def provider(self, info: Info, provider_id: UUID) -> Provider:
        """Get provider by id."""
        provider_dict = await get_provider(provider_id, info)
        return provider_dict

    @strawberry.field
    async def schedules(
        self, info: Info, provider_id: Optional[UUID] = None
    ) -> typing.List[Schedule]:
        """Get all available schedules, optionally filtered to a single provider."""
        schedules_data_list = await get_schedules(info, provider_id)
        return schedules_data_list

    @strawberry.field
    async def schedule(self, info: Info, schedule_id: UUID) -> Schedule:
        """Get schedule by id"""
        schedule_dict = await get_schedule(schedule_id, info)
        return schedule_dict
