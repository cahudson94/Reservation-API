"""."""

from sqlalchemy import delete, insert, select, update, text
from sqlalchemy.orm import subqueryload, load_only

from api.db.session import get_session
from api.db.models import Client as client_model, Appointment as appointment_model
from api.helpers import get_only_selected_fields, get_valid_data
from api.scalars.client_scalar import (
    AddClient,
    Client,
    ClientDeleted,
    ClientNotFound,
    ClientExists,
)


async def get_clients(info):
    """Get all clients, and return given fields."""
    selected_fields = get_only_selected_fields(client_model, info)
    async with get_session() as s:
        sql = text(
            select(client_model)
            .options(load_only(*selected_fields))
            .order_by(client_model.name)
            .__str__()
        )
        db_clients = (await s.execute(sql)).all()

    clients_data_list = []
    for client in db_clients:
        client_dict = get_valid_data(client, client_model)
        client_dict["appointments"] = (
            await s.execute(
                text(
                    select(appointment_model)
                    .where(appointment_model.client_id == client_dict["id"])
                    .__str__()
                ),
                {"client_id_1": client_dict["id"]},
            )
        ).all()
        clients_data_list.append(Client(**client_dict))

    return clients_data_list


async def get_client(client_id, info):
    """Get all clients, and return given fields."""
    selected_fields = get_only_selected_fields(client_model, info)
    async with get_session() as s:
        sql = text(
            select(client_model)
            .options(load_only(*selected_fields))
            .filter(client_model.id == client_id)
            .order_by(client_model.name)
            .__str__()
        )
        db_client = (await s.execute(sql, {"id_1": client_id})).first()

    client_dict = get_valid_data(db_client, client_model)
    client_dict["appointments"] = (
        await s.execute(
            text(
                select(appointment_model)
                .where(appointment_model.client_id == client_dict["id"])
                .__str__()
            ),
            {"client_id_1": client_dict["id"]},
        )
    ).all()
    return Client(**client_dict)


async def add_client(name):
    """Attempt to add an Client to the DB."""
    async with get_session() as s:
        sql = text(select(client_model).filter(client_model.name == name).__str__())
        existing_db_client = (await s.execute(sql, {"name_1": name})).first()
        if existing_db_client is not None:
            return ClientExists()

        query = insert(client_model).values(name=name)
        await s.execute(query)

        sql = text(
            select(client_model)
            .options(load_only(getattr(client_model, "name")))
            .filter(client_model.name == name)
            .__str__()
        )
        db_client = (await s.execute(sql, {"name_1": name})).first()
        await s.commit()

    db_client_serialize_data = db_client._asdict()
    return AddClient(**db_client_serialize_data)


async def delete_client(client_id):
    """Attempt to remove a Client from the DB by ID."""
    async with get_session() as s:
        sql = text(select(client_model).where(client_model.id == client_id).__str__())
        existing_db_user = (await s.execute(sql, {"id_1": client_id})).first()
        if existing_db_user is None:
            return ClientNotFound()

        query = delete(client_model).where(client_model.id == client_id)
        await s.execute(query)
        await s.commit()

    return ClientDeleted()
