from fastapi import APIRouter, Depends

from ..security import check_token


light_router = APIRouter(prefix="/light", tags=["light"], dependencies=[Depends(check_token)])


@light_router.get("/control-panel")
async def get_control_panel():
    pass


@light_router.get("/lamp-data")
async def get_data():
    pass


@light_router.post("/temperature")
async def set_temperature():
    pass


@light_router.post("/brightness")
async def set_brightness():
    pass
