
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class PostInput(BaseModel):
    post_title: str = Field(..., max_length=250)
    post_details: str = Field(..., max_length=500)
    post_it: Optional[bool] = Field(default=True)


class PostOutput(BaseModel):
    id :int
    post_title: str
    post_details: str
    post_it: bool   
    created_time: datetime

    class config:
        orm_mode = True