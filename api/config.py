import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """."""

    PROJECT_TITLE: str = "Appointment Reservation API"
    PROJECT_VERSION: str = "1.0.0"
    HOST_HTTP: str = os.environ.get("HOST_HTTP", "http://")
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    BASE_URL: str = f"{HOST_HTTP}{HOST_URL}:{str(HOST_PORT)}"
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_SERVER: str = os.environ.get("DB_SERVER")
    DB_PORT: int = int(os.environ.get("DB_PORT", 5432))
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    )


settings = Settings()
