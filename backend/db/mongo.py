# backend/db/mongo.py
import motor.motor_asyncio

db = None


async def connect_to_mongo():
    global db
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/igrosine?retryWrites=true&w=majority")
    if client:
        print("Connected to MongoDB")
        db = client.get_database("igrosine")
        return db
    else:
        print("Not Connected to MongoDB")
        return None
