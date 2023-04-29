from fastapi import APIRouter


light_router = APIRouter(prefix="/light", tags=["light"])


@light_router.get("/control-panel")
async def get_control_panel():
    pass


@light_router.get("/temperature")
async def get_temperature():
    pass


@light_router.get("/brightness")
async def get_brightness():
    pass


@light_router.post("/temperature")
async def set_temperature():
    pass


@light_router.post("/brightness")
async def set_brightness():
    pass
