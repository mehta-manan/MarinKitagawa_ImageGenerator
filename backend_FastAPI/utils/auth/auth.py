import jwt
import os

from fastapi import status, HTTPException, Request

from dotenv import load_dotenv
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
exp_time = int(os.getenv("EXP_TIME"))

from database.mongo import database
users_collection =  database["users"]

def verifyJWT(req: Request):
    authorization = req.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing."
        )

    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header."
        )
    
    token = parts[-1]

    try:
        token_payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
    # validate expired token based on "exp"
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired."
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=401,
            detail="Malformed token."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    # validate user
    id = token_payload.get("id")
    if not users_collection.find_one({"id": id}):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user.")

    return token_payload