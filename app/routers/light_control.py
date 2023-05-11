from typing import Annotated
from random import randint
from datetime import datetime

from fastapi import APIRouter, Cookie, Depends

from ..security import verify_token, payload_token
from ..models import LampData, Action
from ..repositories import ActionRepository


light_router = APIRouter(
    prefix="/light", tags=["light"], dependencies=[Depends(verify_token)]
)


@light_router.get("/lamp-data")
async def get_data(lamp_number: int) -> LampData:
    return LampData(
        lamp_number=lamp_number,
        temperature=randint(2700, 6500),
        brightness=randint(0, 100),
    )


@light_router.post("/lamp-data")
async def send_data(
    lamp_data: LampData,
    light_control_token: Annotated[str, Cookie()],
    actions: Annotated[ActionRepository, Depends()],
):
    token_data = payload_token(light_control_token)
    await actions.new_action(
        Action(
            user_id=token_data.sub,
            time=datetime.utcnow(),
            lamp_data=lamp_data
        )
    )