# pylint: disable=too-few-public-methods
"""Shared schema logic and baselines."""
import re
from datetime import timedelta

from pydantic import BaseModel, ConfigDict
from sqlalchemy.inspection import inspect


def from_camel(string):
    """Convert Camel Case to snake case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

def get_only_selected_fields(db_baseclass_name, info):
    """Limit scope of data selection to work within graphql contract."""
    db_relations_fields = inspect(db_baseclass_name).relationships.keys()
    selected_fields = []
    for field in info.selected_fields[0].selections:
        if field.name not in db_relations_fields and from_camel(field.name) not in db_relations_fields:
            try:
                selected_fields.append(getattr(db_baseclass_name, field.name))
            except AttributeError:
                selected_fields.append(getattr(db_baseclass_name, from_camel(field.name)))
    return selected_fields

def get_valid_data(model_data_object, model_class):
    """Convert to dictionary representation of db data."""
    data = {}
    for column in model_class.__table__.columns:
        try:
            data[column.name] = getattr(model_data_object, column.name)
        except:
            pass
    return data

def date_range(start, end):
    times = []
    current = start
    while current < end:
        times.append(current)
        current += timedelta(minutes=15)
    return times
