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
            if await self.get_user(user.email):
                return False

            await self.db.execute(
                f"""
                    INSERT INTO users (
                        email, 
                        firstname,
                        lastname,
                        secondname,
                        password
                    )
                    VALUES (
                        '{user.email}',
                        '{user.firstname.capitalize()}',
                        '{user.lastname.capitalize()}',
                        '{user.secondname.capitalize()}',
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

    async def get_user(self, email: str) -> User | None:
        try:
            cursor = await self.db.execute(
                f"""
                    SELECT * FROM users
                    WHERE email = '{email}'
                """
            )
            if user_row := await cursor.fetchone():
                user = User(
                    email=user_row[0],
                    firstname=user_row[1],
                    lastname=user_row[2],
                    secondname=user_row[3],
                    password=user_row[4],
                )
                return user
            else:
                return None

        except DatabaseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong when getting user! ({e})",
            )
