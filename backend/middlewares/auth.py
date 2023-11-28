from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from backend.config.secrets import SECRET_KEY, ALGORITHM
from backend.db import mongo

async def Auth(request: Request, call_next):
    protected_paths = ["/api/v1/profile","/api/v1/delete-user","/api/v1/update-user","/api/v1/create-video","/api/v1/delete-video/:id"]
    from ..db.mongo import db

    if db is None:
        print("Not connected to MongoDB. Attempting to connect...")
        db = await mongo.connect_to_mongo()

    if request.url.path in protected_paths:
        token = request.cookies.get("token")
        print("Token: ", token)

        if token is None:
            # print("No token found")
            # print("Token Data: ", token)
            error_response = {
                "status": 401,
                "detail": "You're not authorized to access this route"
            }
            return JSONResponse(content=error_response, status_code=401)
        
        else:
            decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            user = await db.get_collection("users").find_one({"email": decode["email"]})

            request.state.user = user
            # print("User in Request: ", request.state.user)
    
    response = await call_next(request)
    return response
