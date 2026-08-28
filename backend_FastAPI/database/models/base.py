from datetime import datetime, timezone
from pydantic import BaseModel, Field

class BaseDBModel(BaseModel):
    # create a new 'timezone-aware UTC datetime' whenever a new instance is created
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 