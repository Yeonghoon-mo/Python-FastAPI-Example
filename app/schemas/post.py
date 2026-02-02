from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base DTO
class PostBase(BaseModel):
    title: str
    content: str

# 생성 DTO
class PostCreate(PostBase):
    pass

# 수정 DTO
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 응답 DTO
class PostResponse(PostBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
