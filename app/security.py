from datetime import date, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from .models import Token, TokenPayload
from .settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def check_token_expire(expire: date) -> bool:
    return date.today() >= expire


def create_token(username: str) -> Token:
    token_payload = TokenPayload(
        sub=username,
        expire=date.today() + timedelta(days=settings.jwt_token_expire_days),
    )
    return Token(
        access_token=jwt.encode(token_payload.dict(), settings.jwt_secret_key)
    )


def get_token_payload(token: str) -> TokenPayload:
    return TokenPayload.parse_obj(jwt.decode(token, settings.jwt_secret_key))
