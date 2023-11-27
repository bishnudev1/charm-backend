from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    name: Optional[str]
    email: str
    password: str
    number: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now().isoformat())
