from typing import Annotated
from datetime import timedelta, datetime

from fastapi import HTTPException, Request, Depends, Cookie
from jose import jwt, JWTError, ExpiredSignatureError

from ..models import Token, TokenPayload
from ..settings import settings
from ..repositories import UserRepository


def create_token(username: str) -> Token:
    token_payload = TokenPayload(
        sub=username,
        exp=datetime.utcnow() + timedelta(days=settings.jwt_token_expire_days),
    )
    return Token(
        access_token=jwt.encode(token_payload.dict(), settings.jwt_secret_key)
    )


def payload_token(token: str) -> TokenPayload:
    return TokenPayload.parse_obj(jwt.decode(token, settings.jwt_secret_key))


async def verify_token(
    *,
    users: Annotated[UserRepository, Depends()],
    light_control_token: Annotated[str, Cookie()],
):
    if not light_control_token:
        raise HTTPException(status_code=401)

    try:
        token_payload = payload_token(light_control_token)
        
        if await users.get_user(token_payload.sub) is None:
            raise JWTError

    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Session expired!")
    except JWTError:
        raise HTTPException(status_code=400, detail="Incorrect token!")


async def check_token(request: Request, users: UserRepository) -> bool:
    try:
        if auth_data := request.cookies.get("light_control_token"):
            await verify_token(light_control_token=auth_data, users=users)
        else:
            return False
    except HTTPException:
        return False

    return True
