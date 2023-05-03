from typing import Annotated
from random import randint

from fastapi import APIRouter, Cookie, Depends

from ..security import verify_token
from ..models import LampData


light_router = APIRouter(
    prefix="/light", tags=["light"], dependencies=[Depends(verify_token)]
)


@light_router.get("/lamp-data")
async def get_data(lamp_number: int) -> LampData:
    return LampData(
        number=lamp_number,
        temperature=randint(2700, 6500),
        brightness=randint(0, 100),
    )


@light_router.post("/lamp-data")
async def send_data(
    lamp_data: LampData, light_control_token: Annotated[str, Cookie()]
):
    print(lamp_data)
