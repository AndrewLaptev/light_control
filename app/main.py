from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi_mqtt import FastMQTT, MQTTConfig

from .settings import settings
from .security import check_token
from .repositories import UserRepository
from .routers import auth_router, light_router
from .libs.sqlite import init_dbms, healthcheck_dbms, db_session


app = FastAPI(title="Light control")
mqtt = FastMQTT(MQTTConfig(host=settings.mqtt_host, port=settings.mqtt_port))

app.include_router(auth_router)
app.include_router(light_router)
app.mount("/static", StaticFiles(directory="front/static"), name="static")


@app.get("/", response_class=HTMLResponse, tags=["root"])
async def get_page(
    request: Request, users: Annotated[UserRepository, Depends()]
):
    if await check_token(request, users):
        with open("front/index.html", "r") as file:
            return file.read()
    else:
        with open("front/login.html", "r") as file:
            return file.read()


@app.on_event("startup")
async def startup_dbms():
    async with asynccontextmanager(db_session)() as db:
        await init_dbms(db)

        if not await healthcheck_dbms(db):
            raise Exception("DBMS healthcheck error!")


@app.on_event("startup")
async def startup_mqtt():
    mqtt.init_app(app)
