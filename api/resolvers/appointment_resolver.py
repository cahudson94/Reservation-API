"""."""

from datetime import datetime, timedelta

from sqlalchemy import delete, insert, select, update, text, or_, and_
from sqlalchemy.orm import subqueryload, load_only

from api.db.session import get_session
from api.db.models import Appointment as appointment_model, Schedule as schedule_model
from api.helpers import get_only_selected_fields, get_valid_data
from api.scalars.appointment_scalar import (
    Appointment,
    AppointmentDeleted,
    AppointmentNotFound,
)


async def get_appointments(info, provider_id):
    """Get all appointments, and return given fields."""
    selected_fields, relationships = get_only_selected_fields(appointment_model, info)
    temp_fields = selected_fields
    if appointment_model.reserve_time not in temp_fields:
        temp_fields.append(appointment_model.reserve_time)
    if appointment_model.id not in temp_fields:
        temp_fields.append(appointment_model.id)
    async with get_session() as s:
        sql = (
            select(appointment_model)
            .options(load_only(*temp_fields))
            .order_by(appointment_model.time)
        )
        status_check = or_(
            appointment_model.status == "avail",
            and_(
                appointment_model.status == "res",
                appointment_model.reserve_time < datetime.now() - timedelta(minutes=30),
            ),
        )
        if provider_id:
            sql = sql.where(
                and_(appointment_model.provider_id == provider_id, status_check)
            )
        else:
            sql = sql.where(status_check)
        db_appointments = (
            await s.execute(
                text(sql.__str__()),
                {
                    "status_1": "avail",
                    "status_2": "res",
                    "reserve_time_1": datetime.now() - timedelta(minutes=30),
                },
            )
        ).all()

    appointments_data_list = []
    for appointment in db_appointments:
        appointment_dict = get_valid_data(appointment, appointment_model)
        if appointment_dict["reserve_time"] < datetime.now() - timedelta(minutes=30):
            await s.execute(
                text(
                    update(appointment_model)
                    .where(appointment_model.id == appointment_dict["id"])
                    .values(status="avail", reserve_time=datetime.min)
                    .__str__()
                ),
                {
                    "id_1": appointment_dict["id"],
                    "status": "avail",
                    "reserve_time": datetime.min,
                },
            )
        if appointment_model.id not in selected_fields:
            del appointment_dict["id"]
        if appointment_model.reserve_time not in selected_fields:
            del appointment_dict["reserve_time"]
        appointments_data_list.append(Appointment(**appointment_dict))
    await s.commit()

    return appointments_data_list


async def get_appointment(appointment_id, info):
    """Get all appointments, and return given fields."""
    selected_fields, relationships = get_only_selected_fields(appointment_model, info)
    async with get_session() as s:
        sql = (
            select(appointment_model)
            .options(load_only(*selected_fields))
            .filter(appointment_model.id == appointment_id)
            .order_by(appointment_model.time)
        )
        db_appointment = (
            await s.execute(text(sql.__str__()), {"id_1": appointment_id})
        ).first()

    appointment_dict = get_valid_data(db_appointment, appointment_model)
    return Appointment(**appointment_dict)


async def add_appointment(provider_id, schedule_id, time):
    """Attempt to add an Appointment to the DB."""
    async with get_session() as s:
        query = insert(appointment_model).values(
            provider_id=provider_id, schedule_id=schedule_id, time=time
        )
        await s.execute(query)

        sql = text(
            select(appointment_model)
            .options(load_only(getattr(appointment_model, "time")))
            .filter(appointment_model.provider_id == provider_id)
            .__str__()
        )
        db_appointment = (
            await s.execute(
                sql, {"provider_id_1": provider_id, "schedule_id_1": schedule_id}
            )
        ).first()

        await s.commit()

    db_appointment_serialize_data = db_appointment._asdict()
    return Appointment(**db_appointment_serialize_data)


async def update_appointment(appointment_id, client_id, status):
    """Attempt to update an Appointment in the DB."""
    async with get_session() as s:
        sql = text(
            select(appointment_model)
            .where(appointment_model.id == appointment_id)
            .__str__()
        )
        existing_db_appointment = (
            await s.execute(sql, {"id_1": appointment_id})
        ).first()
        if existing_db_appointment is None:
            return AppointmentNotFound()

        query = (
            update(appointment_model)
            .where(appointment_model.id == appointment_id)
            .values(client_id=client_id, status=status)
        )
        await s.execute(query)

        db_appointment = (await s.execute(sql, {"id_1": appointment_id})).first()
        await s.commit()

    db_appointment_serialize_data = db_appointment._asdict()
    return Appointment(**db_appointment_serialize_data)


async def delete_appointment(appointment_id):
    """Attempt to remove a Appointment from the DB by ID."""
    async with get_session() as s:
        sql = text(
            select(appointment_model)
            .where(appointment_model.id == appointment_id)
            .__str__()
        )
        existing_db_appointment = (await s.execute(sql)).first()
        if existing_db_appointment is None:
            return AppointmentNotFound()

        query = delete(appointment_model).where(appointment_model.id == appointment_id)
        await s.execute(query)
        await s.commit()

    return AppointmentDeleted()
