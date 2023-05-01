from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from ..models import User, Token
from ..security import create_token
from ..repositories import UserRepository


auth_router = APIRouter(prefix="/auth", tags=["auth"])
UsersRep = Annotated[UserRepository, Depends()]


@auth_router.post("/signup", response_class=RedirectResponse)
async def signup(user: User, users: UsersRep) -> RedirectResponse:
    if not await users.new_user(user):
        raise HTTPException(
            status_code=400, detail="Current user already exist!"
        )
    else:
        return await signin(
            OAuth2PasswordRequestForm(
                username=user.email, password=user.password, scope=""
            ),
            users,
        )


@auth_router.post("/signin", response_class=RedirectResponse)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], users: UsersRep
) -> RedirectResponse:
    token_ = await token(form_data, users)
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="light_control_token",
        value=token_.access_token,
        httponly=True,
    )
    return response


@auth_router.post("/token")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], users: UsersRep
) -> Token:
    if user := await users.get_user(form_data.username):
        if user.password == form_data.password:
            return create_token(user.email)
        else:
            raise HTTPException(status_code=400, detail="Incorrect password!")
    else:
        raise HTTPException(
            status_code=400, detail="Current user does not exist!"
        )
