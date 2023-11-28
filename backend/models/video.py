from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class Video(BaseModel):  
    name: Optional[str]
    likes: Optional[int]
    views: Optional[int]
    hideVideo: Optional[str]
    videoUrl: Optional[str]
    date: Optional[datetime] = Field(default_factory=lambda: datetime.now().isoformat())