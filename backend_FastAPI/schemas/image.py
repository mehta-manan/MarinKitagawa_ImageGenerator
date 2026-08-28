
from datetime import datetime
from pydantic import BaseModel

class ImageBase(BaseModel):
    seed: int | None = None

class PostCreateImageRequestBody(ImageBase):
    prompt_text: str | None = None
    type: str | None = None

class PostCreateImageResponseBody(BaseModel):
    prompt_id: str
    
class GetImageResponseBody(ImageBase):
    prompt_text: str
    s3_url: str
    created_at: datetime
    
class GetImagesResponseBody(BaseModel):
    images: list[GetImageResponseBody]
    total: int