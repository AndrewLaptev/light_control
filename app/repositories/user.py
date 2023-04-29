from typing import Annotated

from aiosqlite import Connection, DatabaseError
from fastapi import HTTPException, Depends

from ..models import User
from ..utils import db_session


class UserRepository:
    def __init__(self, db: Annotated[Connection, Depends(db_session)]):
        self.db = db

    async def new_user(self, user: User) -> bool:
        try:
            if await self.get_user(user.username):
                return False

            await self.db.execute(
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
                        '{user.firstname.capitalize()}',
                        '{user.lastname.capitalize()}',
                        '{user.secondname.capitalize()}',
                        '{user.birthdate}',
                        '{user.password}'
                    );
                """
            )
            await self.db.commit()
        except DatabaseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong when create user! ({e})",
            )

        return True

    async def get_user(self, username: str) -> User | None:
        try:
            cursor = await self.db.execute(
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

        except DatabaseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong when getting user! ({e})",
            )
