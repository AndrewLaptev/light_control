import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite
from aiosqlite import Connection

from .settings import settings


@asynccontextmanager
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


async def init_dbms(db: Connection):
    await db.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                secondname TEXT NULL,
                birthdate TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """
    )
    await db.commit()
    await db.execute(
        """
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY,
                username TEXT,
                time TEXT,
                lamp INTEGER,
                temperature INTEGER,
                brightness INTEGER,
                FOREIGN KEY(username) REFERENCES users(username)
            );
        """
    )
    await db.commit()
    os.system("chmod 777 -R volumes/dbms")
