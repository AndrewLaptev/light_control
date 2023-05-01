from typing import Annotated

from aiosqlite import Connection
from fastapi import HTTPException, Depends

from ..models import Action
from ..utils import db_session


class ActionRepository:
    def __init__(self, db: Annotated[Connection, Depends(db_session)]):
        self.db = db

    async def new_action(self, action: Action):
        try:
            await self.db.execute(
                f"""
                    INSERT INTO actions (
                        user_id,
                        time,
                        lamp,
                        temperature,
                        brightness
                    )
                    VALUES (
                        '{action.user_id}',
                        '{action.time}',
                        '{action.lamp}',
                        '{action.temperature}',
                        '{action.brightness}'
                    );
                """
            )
            await self.db.commit()
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong when create action!",
            )
