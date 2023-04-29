import aiosqlite

from ..models import User
from ..settings import settings


async def new_user(user: User):
    async with aiosqlite.connect(settings.dbms_name) as db:
        pass