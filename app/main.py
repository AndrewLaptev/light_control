from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig

from .settings import settings
from .security import check_token
from .repositories import UserRepository
from .routers import auth_router, light_router
from .logging import init_logging
from .libs.sqlite import init_dbms


init_logging()

app = FastAPI(title="Light control", root_path=settings.root_path)
mqtt = FastMQTT(MQTTConfig(host=settings.mqtt_host, port=settings.mqtt_port))


@app.on_event("startup")
async def startup():
    await init_dbms()


@app.on_event("startup")
async def startup_mqtt():
    mqtt.init_app(app)


app.include_router(auth_router)
app.include_router(light_router)
app.mount("/static", StaticFiles(directory="front/static"), name="static")

templates = Jinja2Templates(directory="front")


@app.get("/", response_class=HTMLResponse, tags=["root"])
async def get_page(
    request: Request, users: Annotated[UserRepository, Depends()]
):
    if await check_token(request, users):
        return templates.TemplateResponse(
            "index.html", {"request": request, "root_path": settings.root_path}
        )
    else:
        return templates.TemplateResponse(
            "login.html", {"request": request, "root_path": settings.root_path}
        )
