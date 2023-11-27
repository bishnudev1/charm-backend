from jose import JWTError, jwt
from backend.config.secrets import SECRET_KEY, ALGORITHM


async def generateToken(user):
    import datetime

    to_encode = {
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt