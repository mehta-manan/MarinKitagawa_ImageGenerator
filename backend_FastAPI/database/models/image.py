from schemas.image import ImageBase
from database.models.base import BaseDBModel

class Image(ImageBase, BaseDBModel):
    prompt_id: str
    status: str
    filename: str | None = None
    s3_key: str | None = None
    created_by: str