from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

# 비밀번호 해싱 설정 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# [비밀번호 검증]
# plain_password: 사용자가 입력한 비번
# hashed_password: DB에 저장된 암호화된 비번
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# [비밀번호 암호화]
def get_password_hash(password):
    return pwd_context.hash(password)

# [JWT 토큰 생성]
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # JWT 서명 (Sign)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
