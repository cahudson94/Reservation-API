"""."""
import strawberry

from api.scalars.appointment_scalar import Appointment, AppointmentDeleted, AppointmentNotFound, AppointmentNotAvailable
from api.scalars.client_scalar import ClientNotFound
from api.scalars.provider_scalar import ProviderNotFound


AddAppointmentResponse = strawberry.union("AddAppointmentResponse", (Appointment, AppointmentNotAvailable, ClientNotFound, ProviderNotFound))
UpdateAppointmentResponse = strawberry.union("UpdateAppointmentResponse", (Appointment, AppointmentNotFound))
DeleteAppointmentResponse = strawberry.union("DeleteAppointmentResponse", (AppointmentDeleted, AppointmentNotFound))
