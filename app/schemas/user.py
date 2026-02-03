from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# [DTO: Data Transfer Object]

# 1. 공통 속성 (Base DTO)
class UserBase(BaseModel):
    # 이메일 정규식 유효성 검사 추가
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# 2. 생성 요청 DTO (Request Body)
class UserCreate(UserBase):
    password: str

# 3. 수정 요청 DTO (Request Body) - [New!]
class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_active: Optional[bool] = None

# 4. 응답 DTO (Response Body)
class User(UserBase):
    is_active: bool
    profile_image_url: Optional[str] = None

    # [ModelMapper] Entity -> DTO 변환
    model_config = ConfigDict(from_attributes=True)
