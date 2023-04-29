from typing import Annotated
from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .models import Token, TokenPayload
from .settings import settings
from .repositories import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_token(username: str) -> Token:
    token_payload = TokenPayload(
        sub=username,
        exp=datetime.utcnow() + timedelta(days=settings.jwt_token_expire_days),
    )
    return Token(
        access_token=jwt.encode(token_payload.dict(), settings.jwt_secret_key)
    )


async def check_token(
    src_token: Annotated[str, Depends(oauth2_scheme)],
    users: Annotated[UserRepository, Depends()],
):
    incorrect_token = HTTPException(status_code=400, detail="Incorrect token!")
    try:
        token_payload = TokenPayload.parse_obj(
            jwt.decode(src_token, settings.jwt_secret_key)
        )
        user = await users.get_user(token_payload.sub)

        if not user or token_payload.exp.timestamp() < datetime.utcnow().timestamp():
            raise incorrect_token
    except JWTError:
        raise incorrect_token
