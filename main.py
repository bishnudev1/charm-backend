from fastapi import FastAPI
from backend.routes import user_routes
from backend.db import mongo
import uvicorn

app = FastAPI()

# @app.on_event("startup")
# async def startup_up_mongo_client():
#     db = await mongo.connect_to_mongo()
#     print(f"Connected to MongoDB: {db.client.server_info}")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_routes.router, prefix="/api/v1")

if __name__ == "__main__" :
    import asyncio

    # Connect to MongoDB before running the server
    asyncio.run(mongo.connect_to_mongo())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
