from fastapi import APIRouter, Depends
router = APIRouter()

from database.mongo import database
tags_collection = database["tags"]

import utils.auth.auth as auth
from schemas.tag import GetTagResponseBody

@router.get("", response_model=list[GetTagResponseBody])
def get_tags(token_payload: dict = Depends(auth.verifyJWT)):
    tags = tags_collection.find()
    return tags