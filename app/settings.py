import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    log_level: str
    log_file_path: str

    root_path: str

    dbms_name: str
    dbms_path: str
    dbms_fullname: Optional[str] = None

    jwt_secret_key: str
    jwt_token_expire_days: int

    lamps_init_temperature: int
    lamps_init_brightness: int

    mqtt_host: str
    mqtt_port: str
    mqtt_topic_lamp_pattern: str
    mqtt_lamp_ids: list[str]
    mqtt_lamp_temp_measure: str
    mqtt_lamp_bright_measure: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
settings.dbms_fullname = os.path.join(settings.dbms_path, settings.dbms_name)
