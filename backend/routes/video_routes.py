from fastapi import APIRouter, Body, Query

from backend.models.video import Video
from ..controllers import video_controllers

router = APIRouter()

@router.get("/video/working")
async def working():
    return await video_controllers.hello()


@router.get("/videos")
async def getAllVideos():
    return await video_controllers.getAllVideos()

@router.get("/get-video/{id}")
async def getVideo(id: str):
    return await video_controllers.getVideo(id)

@router.post('/create-video')
async def createVideo(video: Video):
    return await video_controllers.createVideo(video)

@router.delete('/delete-video/{id}')
async def deleteVideo(id: str):
    return await video_controllers.deleteVideo(id)

