from fastapi import APIRouter
from ..controllers import video_controllers

router = APIRouter()

@router.get("/video/working")
async def working():
    return await video_controllers.hello()

