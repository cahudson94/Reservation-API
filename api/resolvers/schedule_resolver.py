"""."""
from sqlalchemy import delete, insert, select, update, text
from sqlalchemy.orm import subqueryload, load_only, selectinload

from api.db.session import get_session
from api.db.models import Schedule as schedule_model, Appointment as appointment_model
from api.helpers import get_only_selected_fields, get_valid_data
from api.scalars.schedule_scalar import Schedule, ScheduleDeleted, ScheduleNotFound


async def get_schedules(info, provider_id):
	"""Get all schedules, and return given fields."""
	selected_fields = get_only_selected_fields(schedule_model, info)
	async with get_session() as s:
		sql = select(schedule_model).options(load_only(*selected_fields)).order_by(schedule_model.start)
		if provider_id:
			sql = sql.where(schedule_model.provider_id == provider_id)
		db_schedules = (await s.execute(text(sql.__str__()))).all()

		schedules_data_list = []
		for schedule in db_schedules:
			schedule_dict = get_valid_data(schedule, schedule_model)
			schedule_dict["appointments"] = (await s.execute(text(select(appointment_model).where(appointment_model.schedule_id == schedule_dict["id"]).__str__()), {"schedule_id_1": schedule_dict["id"]})).all()
			print(schedule_dict["appointments"])
			schedules_data_list.append(Schedule(**schedule_dict))



	return schedules_data_list

async def get_schedule(schedule_id, info):
	"""Get all schedules, and return given fields."""
	selected_fields = get_only_selected_fields(schedule_model, info)
	async with get_session() as s:
		sql = text(select(schedule_model).options(load_only(*selected_fields)).filter(schedule_model.id == schedule_id) \
		.order_by(schedule_model.start).__str__())
		db_schedule = (await s.execute(sql, {"id_1": schedule_id})).first()

	schedule_dict = get_valid_data(db_schedule, schedule_model)
	schedule_dict["appointments"] = (await s.execute(text(select(appointment_model).where(appointment_model.schedule_id == schedule_dict["id"]).__str__()), {"schedule_id_1": schedule_dict["id"]})).all()
	return Schedule(**schedule_dict)

async def add_schedule(provider_id, start, end):
	"""Attempt to add a Schedule to the DB."""
	async with get_session() as s:
		query = insert(schedule_model).values(provider_id=provider_id, start=start, end=end)
		await s.execute(query)
		
		sql = text(select(schedule_model).options(load_only(getattr(schedule_model, 'start'), getattr(schedule_model, 'end'))).filter(schedule_model.provider_id == provider_id).__str__())
		db_schedule = (await s.execute(sql, {"provider_id_1": provider_id, })).first()
		await s.commit()

	db_schedule_serialize_data = db_schedule._asdict()
	return Schedule(**db_schedule_serialize_data)

async def update_schedule(schedule_id, start, end):
	"""Attempt to update a Schedule in the DB by ID."""
	async with get_session() as s:
		sql = text(select(schedule_model).where(schedule_model.id == schedule_id).__str__())
		existing_db_schedule = (await s.execute(sql)).first()
		if existing_db_schedule is None:
			return ScheduleNotFound()

		query = delete(appointment_model).where(appointment_model.schedule_id == schedule_id)
		await s.execute(query)
		query = update(schedule_model).where(schedule_model.id == schedule_id).values(start=start, end=end)
		await s.execute(query)

		sql = text(select(schedule_model).where(schedule_model.id == schedule_id).__str__())
		db_stickynote = (await s.execute(sql, {"id_1": schedule_id})).first()
		await s.commit()

	db_schedule_serialize_data = db_stickynote._asdict()
	return Schedule(**db_schedule_serialize_data)

async def delete_schedule(schedule_id):
	"""Attempt to remove a Schedule from the DB by ID."""
	async with get_session() as s:
		sql = text(select(schedule_model).where(schedule_model.id == schedule_id).__str__())
		existing_db_user = (await s.execute(sql)).first()
		if existing_db_user is None:
			return ScheduleNotFound()

		query = delete(schedule_model).where(schedule_model.id == schedule_id)
		await s.execute(query)
		await s.commit()
	
	return ScheduleDeleted()