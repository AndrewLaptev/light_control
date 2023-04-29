from aiosqlite import Connection

from fastapi import HTTPException

from ..models import User


async def new_user(db: Connection, user: User) -> bool:
    try:
        if await get_user(db, user.username):
            return False

        await db.execute(
            f"""
                INSERT INTO users (
                    username, 
                    firstname,
                    lastname,
                    secondname,
                    birthdate,
                    password
                )
                VALUES (
                    '{user.username}',
                    '{user.firstname}',
                    '{user.lastname}',
                    '{user.secondname}',
                    '{user.birthdate}',
                    '{user.password}'
                );
            """
        )
        await db.commit()
    except Exception:
        raise HTTPException(
            status_code=500, detail="Something went wrong when create user!"
        )

    return True


async def get_user(db: Connection, username: str) -> User | None:
    try:
        cursor = await db.execute(
            f"""
                SELECT * FROM users
                WHERE username = '{username}'
            """
        )
        if user_row := await cursor.fetchone():
            user = User(
                username=user_row[0],
                firstname=user_row[1],
                lastname=user_row[2],
                secondname=user_row[3],
                birthdate=user_row[4],
                password=user_row[5],
            )
            return user
        else:
            return None

    except Exception:
        raise HTTPException(
            status_code=500, detail="Something went wrong when getting user!"
        )
