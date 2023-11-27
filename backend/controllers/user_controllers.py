# User Label Controllers
from datetime import datetime
from backend.db import mongo
from backend.models.user import User
from backend.utils.hash import hash_password, compare_password
from backend.utils.token import generateToken
from fastapi import Request, Response

async def hello():
    return {
        "status": 200,
        "data": "Server is running"
    }


def getProfile(request:Request):
    state = request.state.user
    user = User(**state)
    return {
        "status": 200,
        "data": user
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

async def loginUser(response:Response,user):
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
    
    token = await generateToken(isExistingUser)

    response.set_cookie(key="token", value=token)

    return {
        "status": 200,
        "data": f"Welcome back {isExistingUser['name']}"
    }

def logoutUser(response:Response):
    response.delete_cookie(key="token")
    return {
        "status": 200,
        "data": "Logged Out"
    }

async def deleteProfile(response:Response, request:Request,body):
    from ..db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    state = request.state.user
    user = User(**state)

    userCollection = db.get_collection("users")

    isExistingUser = await userCollection.find_one({"email": user.email})

    if(isExistingUser == None):
        return {
            "status": 400,
            "data": "User doesn't exists"
        }
    
    correctPassword = compare_password(body["password"], isExistingUser["password"])

    if(correctPassword == False):
        return {
            "status": 400,
            "data": "Incorrect Credintials"
        }
    
    await userCollection.delete_one({"email": user.email})
    
    response.delete_cookie(key="token")

    return {
        "status": 200,
        "data": "User Deleted"
    }

async def updateProfile(request: Request,response: Response, body):
    from ..db.mongo import db  # Import 'db' explicitly

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    state = request.state.user
    user = User(**state)

    userCollection = db.get_collection("users")

    isExistingUser = await userCollection.find_one({"email": user.email})

    if(isExistingUser == None):
        return {
            "status": 400,
            "data": "User doesn't exists"
        }
    
    if(body["name"]):
        isExistingUser["name"] = body["name"]

    if(body["email"]):
        isExistingUser["email"] = body["email"]

    if(body["number"]):
        isExistingUser["number"] = body["number"]

    if(body["password"]):
        isExistingUser["password"] = hash_password(body["password"])

    await userCollection.update_one({"email": user.email}, {"$set": isExistingUser})

    response.delete_cookie(key="token")

    return {
        "status": 200,
        "data": "User Updated"
    }