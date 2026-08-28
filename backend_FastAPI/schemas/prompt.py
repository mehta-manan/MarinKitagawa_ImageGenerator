from pydantic import BaseModel

class PromptBase(BaseModel):
    id: str
    text: str