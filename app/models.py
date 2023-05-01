from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    secondname: str | None = None
    password: str


class Action(BaseModel):
    user_id: str
    time: datetime
    lamp: int
    temperature: int
    brightness: int


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime | None = None
