from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core import security
from app.core.config import settings
from app.repository import user_repository

# [Spring: AuthService]

def login(db: Session, form_data):
    # 1. 유저 확인
    user = user_repository.get_user(db, email=form_data.username)
    
    # 2. 비밀번호 검증
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. 토큰 발급
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
