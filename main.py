"""."""

import load_env
from api.config import settings
import asyncio
import uvicorn
from api.db.session import engine
from api.db.populate import create_tables
from api.api import create_api

application = create_api()
asyncio.run(create_tables(engine))
