from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Cookie, Depends

from ...models import LampData, Action
from ...services import LampControl
from ...repositories import ActionRepository
from ...libs.security import verify_token, payload_token


light_router = APIRouter(
    prefix="/api/light", tags=["light"], dependencies=[Depends(verify_token)]
)
lamp_control = LampControl()


@light_router.get("/lamp-data")
async def get_data(lamp_number: int) -> LampData:
    return lamp_control.get_lamp_data(lamp_number)


@light_router.post("/lamp-data")
async def set_data(
    lamp_data: LampData,
    light_control_token: Annotated[str, Cookie()],
    actions: Annotated[ActionRepository, Depends()],
):
    lamp_control.set_lamp_data(lamp_data)
    token_data = payload_token(light_control_token)
    await actions.new_action(
        Action(
            user_id=token_data.sub, time=datetime.utcnow(), lamp_data=lamp_data
        )
    )
