from pydantic import BaseModel

class GetTagResponseBody(BaseModel):
    name: str
    value: str
    type: str
    is_nsfw: bool