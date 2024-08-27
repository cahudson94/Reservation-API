"""."""
from sqlalchemy import delete, insert, select, update, text
from sqlalchemy.orm import subqueryload, load_only

from api.db.session import get_session
from api.db.models import Provider as provider_model, Schedule as schedule_model
from api.helpers import get_only_selected_fields, get_valid_data
from api.scalars.provider_scalar import Provider, ProviderDeleted, ProviderNotFound, ProviderExists

async def get_providers(info):
	"""Get all providers, and return given fields."""
	selected_fields = get_only_selected_fields(provider_model, info)
	async with get_session() as s:
		sql = text(select(provider_model).options(load_only(*selected_fields)).order_by(provider_model.name).__str__())
		db_providers = (await s.execute(sql)).all()

	providers_data_list = []
	for provider in db_providers:
		provider_dict = get_valid_data(provider, provider_model)
		provider_dict["schedules"] = (await s.execute(text(select(schedule_model).where(schedule_model.provider_id == provider_dict["id"]).__str__()), {"provider_id_1": provider_dict["id"]})).all()
		providers_data_list.append(Provider(**provider_dict))

	return providers_data_list

async def get_provider(provider_id, info):
	"""Get all providers, and return given fields."""
	selected_fields = get_only_selected_fields(provider_model, info)
	async with get_session() as s:
		sql = text(select(provider_model).options(load_only(*selected_fields)).filter(provider_model.id == provider_id) \
		.order_by(provider_model.name).__str__())
		db_provider = (await s.execute(sql, {"id_1": provider_id})).first()
	
	provider_dict = get_valid_data(db_provider, provider_model)
	provider_dict["schedules"] = (await s.execute(text(select(schedule_model).where(schedule_model.provider_id == provider_dict["id"]).__str__()), {"provider_id_1": provider_dict["id"]})).all()
	return Provider(**provider_dict)

async def add_provider(name):
	"""Attempt to add an Provider to the DB."""
	async with get_session() as s:
		sql = text(select(provider_model) \
			.filter(provider_model.name == name).__str__())
		existing_db_provider = (await s.execute(sql, {"name_1": name})).first()
		if existing_db_provider is not None:
			return ProviderExists()

		query = insert(provider_model).values(name=name)
		await s.execute(query)
		
		sql = text(select(provider_model).options(load_only(getattr(provider_model, 'name'))).filter(provider_model.name == name).__str__())
		db_provider = (await s.execute(sql, {"name_1": name})).first()
		await s.commit()

	db_provider_serialize_data = db_provider._asdict()
	return Provider(**db_provider_serialize_data)

async def delete_provider(provider_id):
	"""Attempt to remove a Provider from the DB by ID."""
	async with get_session() as s:
		sql = text(select(provider_model).where(provider_model.id == provider_id).__str__())
		existing_db_user = (await s.execute(sql, {"id_1": provider_id})).first()
		if existing_db_user is None:
			return ProviderNotFound()

		query = delete(provider_model).where(provider_model.id == provider_id)
		await s.execute(query)
		await s.commit()
	
	return ProviderDeleted()
