from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DATABASE_URL = "sqlite+aiosqlite:///./fastapi.db"


class Settings(BaseSettings):
    app_title: str = "QRkot"
    description: str = "Благотворительный фонд поддержки котиков QRKot"
    database_url: str = DATABASE_URL
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    yandex_disk_token: Optional[str] = None
    report_format: str = "%Y/%m/%d %H:%M:%S"
    secret: str = "SECRET"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
