import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    dbms_name: str
    dbms_path: str
    dbms_fullname: str | None = None

    jwt_secret_key: str
    jwt_token_expire_days: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
settings.dbms_fullname = os.path.join(settings.dbms_path, settings.dbms_name)
