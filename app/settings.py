import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    log_level: str
    log_file_path: str

    root_path: str

    dbms_name: str
    dbms_path: str
    dbms_fullname: str | None = None

    jwt_secret_key: str
    jwt_token_expire_days: int

    mqtt_host: str
    mqtt_port: str
    mqtt_topic_lamp: str
    mqtt_lamp_ids: str
    mqtt_lamp_idl: list[str] | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
settings.dbms_fullname = os.path.join(settings.dbms_path, settings.dbms_name)
settings.mqtt_lamp_idl = settings.mqtt_lamp_ids.split(",")
