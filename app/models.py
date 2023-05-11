from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    secondname: str | None = None
    password: str


class LampData(BaseModel):
    lamp_number: int
    temperature: int = 2700
    brightness: int = 0


class Action(BaseModel):
    user_id: str
    time: datetime
    lamp_data: LampData


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime | None = None
