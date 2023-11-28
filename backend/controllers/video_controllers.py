from fastapi.responses import JSONResponse
from backend.db import mongo
from backend.models.video import Video

async def hello():
    return {
        "status": 200,
        "data": "Server is running"
    }

async def getVideo(id):
    from backend.db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    videoCollection = db.get_collection("videos")

    resp = await videoCollection.find_one({"videoUrl": id})

    if resp is None:
        return JSONResponse(content={"status": 404, "data": "Video not found"}, status_code=404)

    video = Video(**resp)

    return {
        "status": 200,
        "data": video
    }

async def getAllVideos():
    from backend.db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    videoCollection = db.get_collection("videos")

    resp = await videoCollection.find().to_list(length=100)

    videos = []

    for video_data in resp:
        video_model = Video(**video_data)
        videos.append(video_model)

    return {
        "status": 200,
        "data": videos
    }

async def createVideo(video: Video):
    from backend.db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    videoCollection = db.get_collection("videos")


    isExist = await videoCollection.find_one({"videoUrl": video.videoUrl})

    if isExist:
        return {
            "status": 400,
            "data": "Video already exists"
        }

    resp = await videoCollection.insert_one(video.model_dump())

    if(resp.inserted_id):
        return {
            "status": 200,
            "data": "Video created successfully"
        }

    return {
        "status": 400,
        "data": "Failed to create video"
    }


async def deleteVideo(id):
    from backend.db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    print("Video: ", id)

    videoCollection = db.get_collection("videos")

    resp = await videoCollection.delete_one({"videoUrl": id})

    if(resp.deleted_count):
        return {
            "status": 200,
            "data": "Video deleted successfully"
        }

    return {
        "status": 400,
        "data": "Failed to delete video"
    }