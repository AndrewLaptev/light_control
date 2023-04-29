from fastapi import FastAPI

from .routers import auth_router, light_router
from .utils import init_dbms, healthcheck_dbms


app = FastAPI(title="Light control")

app.include_router(auth_router)
app.include_router(light_router)


@app.on_event("startup")
async def startup_dbms():
    await init_dbms()

    if not await healthcheck_dbms():
        raise Exception("DBMS healthcheck error!")