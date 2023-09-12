from typing import Annotated

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from ..settings import settings
from ..repositories import UserRepository
from ..libs.security import check_token, verify_token
from ..libs.pager import Pager


front_router = APIRouter(tags=["frontend"])
templates = Jinja2Templates(directory="front/templates")
pager = Pager(dir_path="front/pages")


@front_router.get("/", response_class=RedirectResponse)
async def page_distributor(
    request: Request, users: Annotated[UserRepository, Depends()]
) -> RedirectResponse:
    if await check_token(request, users):
        page_path = settings.full_location("main")
    else:
        page_path = settings.full_location("login")

    return RedirectResponse(page_path, status_code=status.HTTP_302_FOUND)


@front_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "root_path": settings.root_path,
        },
    )


@front_router.get(
    "/main", response_class=HTMLResponse, dependencies=[Depends(verify_token)]
)
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "root_path": settings.root_path,
            "page": pager.get_page("main"),
        },
    )


@front_router.get(
    "/plan", response_class=HTMLResponse, dependencies=[Depends(verify_token)]
)
async def plan_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "root_path": settings.root_path,
            "page": pager.get_page("plan"),
        },
    )
