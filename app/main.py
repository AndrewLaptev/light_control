from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import auth_router, light_router
from .utils import init_dbms, healthcheck_dbms, db_session


app = FastAPI(title="Light control")

app.include_router(auth_router)
app.include_router(light_router)


@app.on_event("startup")
async def startup_dbms():
    async with asynccontextmanager(db_session)() as db:
        await init_dbms(db)

        if not await healthcheck_dbms(db):
            raise Exception("DBMS healthcheck error!")
