import random
import uuid

import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, status, Query, Depends, BackgroundTasks
router = APIRouter()

from database.mongo import database
collections = {"images": database["images"], "prompts": database["prompts"]}

import utils.auth.auth as auth
from schemas.image import PostCreateImageRequestBody, PostCreateImageResponseBody, GetImagesResponseBody
from clients.comfyui_http import comfyui_http_client
from clients.comfyui_ws import comfyui_ws_client
from clients.s3 import s3
from constants.comfyui import SEED_MIN, SEED_MAX, DEFAULT_PROMPT, DEFAULT_TYPE, SUPPORTED_TYPES

@router.get("", response_model=GetImagesResponseBody)
def get_images(
    page_num: int = Query(1, ge=1), 
    page_size: int = Query(5, ge=1),
    token_payload: dict = Depends(auth.verifyJWT)
    ):
    
    user_id = token_payload["id"]
    
    skip = (page_num - 1) * page_size

    # separate query to get count
    total = collections["images"].count_documents({
        "created_by": user_id
    })

    # paginate before join (lookup) to optimize query performance
    pipeline = [
        {
            "$match": {
                "created_by": user_id
            }
        },
        {
            "$sort": {
                "created_at": -1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": page_size
        },
        {
            "$lookup": {
                "from": "prompts",
                "localField": "prompt_id",
                "foreignField": "id",
                "as": "prompt"
            }
        },
        {
            "$unwind": "$prompt"
        },
        {
            "$project": {
                "_id": 0,
                "prompt_text": "$prompt.text",
                "s3_key": 1,
                "created_at": 1,
                "seed": 1
            }
        }
    ]

    images = collections["images"].aggregate(pipeline)
    
    return {
        "total" : total,
        "images": [
        {
            "prompt_text": image["prompt_text"],
            "s3_url": s3.get_image_url(image["s3_key"]),
            "created_at": image["created_at"],
            "seed": image["seed"]
        }
        for image in images
    ]}
    
@router.post("/generate", response_model=PostCreateImageResponseBody, status_code=status.HTTP_201_CREATED)
async def create_image(
    background_tasks: BackgroundTasks,
    body: PostCreateImageRequestBody,
    token_payload: dict = Depends(auth.verifyJWT)
    ):
    
    seed = body.seed
    prompt_text = body.prompt_text
    type = body.type

    logger.info(f"Seed received from request: {seed}")

    if seed is None:
        seed = random.randint(SEED_MIN, SEED_MAX)
        logger.debug(f"No seed provided. Generated random seed: {seed}")

    if not prompt_text:
        prompt_text = DEFAULT_PROMPT
        logger.debug(f"No prompt provided. Using default prompt: {DEFAULT_PROMPT}")
        
    if type not in SUPPORTED_TYPES:
        type = DEFAULT_TYPE
        logger.debug(f"Invalid or no type provided. Using default type: {DEFAULT_TYPE}")

    comfyui_client = comfyui_ws_client if type == "ws" else comfyui_http_client
    client_id = str(uuid.uuid4()) if type == "ws" else None
    logger.info(f"Using type: {type}")
    logger.info(f"Using client_id: {client_id}")
    
    prompt_id = comfyui_client.queue_image(prompt_text, seed, client_id, None)
    
    user = {"id": token_payload["id"], "email": token_payload["email"]}
    prompt = {"id": prompt_id, "text": prompt_text}

    # asyncio.create_task(comfyui_http_client.generate_image(user, prompt, seed, collections, client_id))
    background_tasks.add_task(comfyui_client.generate_image, user, prompt, seed, collections, client_id)

    return {"prompt_id": prompt_id}


