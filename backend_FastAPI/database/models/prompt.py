from schemas.prompt import PromptBase
from database.models.base import BaseDBModel

class Prompt(PromptBase, BaseDBModel):
    created_by: str