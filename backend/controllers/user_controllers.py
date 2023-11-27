# User Label Controllers
from datetime import datetime
from backend.db import mongo
from bson import json_util, ObjectId
import bcrypt
from backend.models.user import User
from backend.utils.hash import hash_password, compare_password

async def hello():
    return {
        "status": 200,
        "data": "Server is running"
    }

async def getUsers():
    from ..db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    userCollection = db.get_collection("users")
    cursor = userCollection.find()

    users = []

    for user_data in await cursor.to_list(length=100):
        user_model = User(**user_data)
        users.append(user_model)

    print(users)

    return {
        "status": 200,
        "data": users
    }

async def createUser(user: User):

    from ..db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    userCollection = db.get_collection("users")

    isExistingUser = await userCollection.find_one({"email": user.email})

    if(isExistingUser):
        return {
            "status": 400,
            "data": "User already exists"
        }
    
    user.password = hash_password(user.password)

    await userCollection.insert_one(user.model_dump())

    return {
        "status": 200,
        "data": user
    }

async def loginUser(user):
    from ..db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    userCollection = db.get_collection("users")

    isExistingUser = await userCollection.find_one({"email": user["email"]})

    if(isExistingUser == None):
        return {
            "status": 400,
            "data": "User doesn't exists"
        }
    
    correctPassword = compare_password(user["password"], isExistingUser["password"])

    if(correctPassword == False):
        return {
            "status": 400,
            "data": "Incorrect Credintials"
        }
    
    return {
        "status": 200,
        "data": f"Welcome back {isExistingUser['name']}"
    }

