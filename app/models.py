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
    username: str
    time: datetime
    lamp: int
    temperature: int
    brightness: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime | None = None
