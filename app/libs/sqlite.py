import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiosqlite
from aiosqlite import Connection

from ..settings import settings


async def db_session() -> AsyncGenerator[Connection, None]:
    db = await aiosqlite.connect(settings.dbms_fullname)
    try:
        yield db
    finally:
        await db.close()


async def healthcheck_dbms(db: Connection) -> bool:
    try:
        await db.execute("SELECT 1 FROM users")
        await db.execute("SELECT 1 FROM actions")
    except Exception:
        return False
    return True


async def create_dbms(db: Connection):
    await db.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                secondname TEXT NULL,
                password TEXT NOT NULL
            );
        """
    )
    await db.commit()
    await db.execute(
        """
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                time TEXT,
                lamp INTEGER,
                temperature INTEGER,
                brightness INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(email)
            );
        """
    )
    await db.commit()

    if oct(os.stat(settings.dbms_fullname).st_mode)[-3:] != "777":
        os.system("chmod 777 -R volumes/dbms")


async def init_dbms():
    async with asynccontextmanager(db_session)() as db:
        await create_dbms(db)

        if not await healthcheck_dbms(db):
            raise Exception("DBMS healthcheck error!")
