from fastapi import APIRouter, Depends
router = APIRouter()

from database.mongo import database
users_collection = database["users"]

import utils.auth.auth as auth
from schemas.user import GetUserResponseBody

@router.get("", response_model=GetUserResponseBody)
def get_user(token_payload: dict = Depends(auth.verifyJWT)):
    user = users_collection.find_one({"id": token_payload["id"]})
    return user