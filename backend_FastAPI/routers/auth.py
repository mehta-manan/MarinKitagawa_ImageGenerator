import os
import jwt

from fastapi import APIRouter, status, HTTPException, Request
router = APIRouter()

from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
exp_time = int(os.getenv("EXP_TIME"))

from database.mongo import database
users_collection =  database["users"]

import utils.auth.auth as auth
from database.models.user import User
from schemas.user import PostSignupUserRequestBody, PostSignupUserResponseBody, PostSigninUserRequestBody, PostSigninUserResponseBody

@router.post("/signup", response_model=PostSignupUserResponseBody, status_code=status.HTTP_201_CREATED)
def signup(body: PostSignupUserRequestBody):
    # validate username
    if users_collection.find_one({"id": body.id}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already exists.")

    # validate email
    if users_collection.find_one({"email": body.email}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    # hash password
    hash_password = password_hash.hash(body.password)

    # create new user
    new_user = User(
        id=body.id,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        age=body.age,
        hash_password=hash_password).model_dump()

    # save user to db
    users_collection.insert_one(new_user)

    # generate jwt
    exp = datetime.now() + timedelta(minutes=exp_time)
    token = jwt.encode({"id":body.id, "email":body.email, "exp":exp.timestamp()}, secret_key, algorithm)

    # return token
    return {"jwt":token}

@router.post("/signin", response_model=PostSigninUserResponseBody)
def signin(body: PostSigninUserRequestBody):
    # handle case for both present and both absent
    if bool(body.id) == bool(body.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide either user ID or email, not both.")

    # login using user ID
    if body.id:
        user = users_collection.find_one({"id": body.id})

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist.")

    # login using email
    else:
        user = users_collection.find_one({"email": body.email})

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User (Email) does not exist.")

    # verify password
    if not password_hash.verify(body.password, user["hash_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")

    # generate jwt
    exp = datetime.now() + timedelta(minutes=exp_time)
    token = jwt.encode({"id":user["id"], "email":user["email"], "exp":exp.timestamp()}, secret_key, algorithm)

    # return token
    return {"jwt":token}

@router.get("/verify")
def verifyJWT(req: Request):
    return auth.verifyJWT(req)