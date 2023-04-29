from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models import User, Token
from ..security import create_token
from ..repositories import UserRepository


auth_router = APIRouter(prefix="/auth", tags=["auth"])
UsersRep = Annotated[UserRepository, Depends()]


@auth_router.post("/register")
async def register(user: User, users: UsersRep) -> Token:
    if not await users.new_user(user):
        raise HTTPException(
            status_code=400, detail="Current user already exist!"
        )
    else:
        return await login(
            OAuth2PasswordRequestForm(
                username=user.username, password=user.password, scope=""
            ),
            users,
        )


@auth_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], users: UsersRep
) -> Token:
    if user := await users.get_user(form_data.username):
        if user.password == form_data.password:
            return create_token(user.username)
        else:
            raise HTTPException(status_code=400, detail="Incorrect password!")
    else:
        raise HTTPException(
            status_code=400, detail="Current user does not exist!"
        )
