from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from ...settings import settings
from ...models import User
from ...repositories import UserRepository
from ...libs.security import create_token


auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
UsersRep = Annotated[UserRepository, Depends()]


@auth_router.post("/signin", response_class=RedirectResponse, status_code=302)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], users: UsersRep
) -> RedirectResponse:
    token_ = await create_token(form_data, users)
    response = RedirectResponse(
        settings.full_location("main"), status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key="light_control_token",
        value=token_.access_token,
        path=settings.root_path,
        httponly=True,
    )
    return response


@auth_router.get("/signout", response_class=RedirectResponse, status_code=302)
async def signout() -> RedirectResponse:
    response = RedirectResponse(
        settings.root_path, status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie(key="light_control_token", path=settings.root_path)
    return response


@auth_router.post("/signup", response_class=RedirectResponse, status_code=302)
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
