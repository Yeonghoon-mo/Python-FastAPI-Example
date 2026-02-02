from pydantic import BaseModel, ConfigDict


# 공통 속성 (Base)
class UserBase(BaseModel):
    email: str

# 데이터 생성 시 필요한 속성 (비밀번호 포함)
class UserCreate(UserBase):
    password: str

# 데이터 조회 시 보여줄 속성 (비밀번호 제외, ID 포함)
class User(UserBase):
    id: int
    is_active: bool

    # ORM 객체(User 모델)를 Pydantic 객체로 변환 허용
    class Config:
        model_config = ConfigDict(from_attributes=True)