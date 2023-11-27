# User Level Routes

from fastapi import APIRouter, Body, Request, Response

from backend.models.user import User
from ..controllers import user_controllers

router = APIRouter()

@router.get("/working")
async def working():
    return await user_controllers.hello()

@router.get("/users")
async def read_users():
    return await user_controllers.getUsers()

@router.get("/profile")
def read_profile(request:Request):
    return user_controllers.getProfile(request)

@router.post("/create-user")
async def create_user(user: User):
    return await user_controllers.createUser(user)

@router.post("/login-user")
async def create_user(response:Response,user: object = Body(...)):
    return await user_controllers.loginUser(response,user)

@router.get("/logout")
def logout_user(response:Response):
    return user_controllers.logoutUser(response)

@router.put("/update-user")
async def update_user(request:Request,response: Response, user: object = Body(...)):
    return await user_controllers.updateProfile(request,response,user)

@router.delete("/delete-user")
async def delete_user(response:Response, request:Request,user: object = Body(...)):
    return await user_controllers.deleteProfile(response, request,user)
