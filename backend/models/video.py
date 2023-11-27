from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Video([BaseModel]):  
    name: Optional[str]
    likes: Optional[int]
    views: Optional[str]
    hideVideo: Optional[bool]
    videoUrl: Optional[str]
    date: Optional[datetime] = Field(default_factory=lambda: datetime.now().isoformat())