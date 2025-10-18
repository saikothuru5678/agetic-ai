from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    text: str = Field(..., min_length=3, max_length=5000)

class FeedbackOut(BaseModel):
    id: int
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    text: str
    sentiment: str
    category: str
    department: str
    created_at: datetime

    class Config:
        orm_mode = True