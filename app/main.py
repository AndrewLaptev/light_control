from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .settings import settings
from .services import LampControl
from .routers import front_router
from .routers.api import auth_router, light_router
from .logging import init_logging
from .libs.sqlite import init_dbms


init_logging()

app = FastAPI(title="Light control", root_path=settings.root_path)
lamp_control = LampControl()


@app.on_event("startup")
async def startup():
    await init_dbms()
    await lamp_control.mqtt.connection()
    lamp_control.init_lamps(
        settings.lamps_init_temperature, settings.lamps_init_brightness
    )


@app.on_event("shutdown")
async def shutdown():
    lamp_control.shutdown_lamps()
    await lamp_control.mqtt.client.disconnect()


app.include_router(auth_router)
app.include_router(light_router)
app.include_router(front_router)
app.mount("/static", StaticFiles(directory="front/static"), name="static")
