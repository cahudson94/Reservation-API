"""."""
import load_env
from api.config import settings
import asyncio
import uvicorn
from api.db.session import engine
from api.db.populate import create_tables
from api.api import create_api

application = create_api()

if __name__ == "__main__":
    """."""
    print("Populating database...")
    asyncio.run(create_tables(engine))
    print("Database populated.")

    print("Starting server...")
    uvicorn.run("main:application", host=settings.HOST_URL, port=settings.HOST_PORT, reload=True)
