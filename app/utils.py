import aiosqlite

from .settings import settings


async def healthcheck_dbms() -> bool:
    async with aiosqlite.connect(settings.dbms_fullname) as db:
        try:
            await db.execute("SELECT 1 FROM users")
            await db.execute("SELECT 1 FROM actions")
        except Exception:
            return False
        return True


async def init_dbms():
    async with aiosqlite.connect(settings.dbms_fullname) as db:
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
