from pydantic import BaseModel

# 토큰 응답 DTO
class Token(BaseModel):
    access_token: str
    token_type: str

# 토큰 데이터 (Payload)
class TokenData(BaseModel):
    email: str | None = None
