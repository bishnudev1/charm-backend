# User Level Routes

from fastapi import APIRouter, Body

from backend.models.user import User
from ..controllers import user_controllers

router = APIRouter()

@router.get("/working")
async def working():
    return await user_controllers.hello()

@router.get("/users")
async def read_users():
    return await user_controllers.getUsers()

@router.post("/create-user")
async def create_user(user: User):
    return await user_controllers.createUser(user)

@router.post("/login-user")
async def create_user(user: object = Body(...)):
    return await user_controllers.loginUser(user)