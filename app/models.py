from pydantic import BaseModel
from datetime import datetime, date


class User(BaseModel):
    username: str
    firstname: str
    lastname: str
    secondname: str | None = None
    birthdate: date
    password: str


class Action(BaseModel):
    user_id: int
    time: datetime
    lamp: int
    temperature: int
    brightness: int
