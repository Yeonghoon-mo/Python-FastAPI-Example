from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repository import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.tasks.email_task import send_welcome_email

# [Spring: @Service]

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = await user_repository.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일 계정입니다.")
    
    new_user = await user_repository.create_user(db=db, user=user)
    
    # 회원가입 성공 시 웰컴 이메일 발송 (비동기 Task)
    send_welcome_email.delay(new_user.email)
    
    return new_user

async def get_user(db: AsyncSession, email: str):
    db_user = await user_repository.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="해당 Email의 유저가 존재하지 않습니다.")
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await user_repository.get_users(db, skip=skip, limit=limit)

# 유저 수정
async def update_user(db: AsyncSession, email: str, user_update: UserUpdate):
    # 1. 수정할 유저가 존재하는지 확인
    db_user = await get_user(db, email) # 없으면 여기서 404 발생
    
    # 2. 업데이트 수행
    return await user_repository.update_user(db=db, db_user=db_user, user_update=user_update)

# 유저 삭제
async def delete_user(db: AsyncSession, email: str):
    # 1. 삭제할 유저가 존재하는지 확인
    db_user = await get_user(db, email) # 없으면 여기서 404 발생
    
    # 2. 삭제 수행
    await user_repository.delete_user(db=db, db_user=db_user)
    return {"유저 삭제 완료.": db_user}

# 프로필 이미지 업데이트
async def update_profile_image(db: AsyncSession, email: str, image_url: str):
    db_user = await get_user(db, email)
    db_user.profile_image_url = image_url
    await db.commit()
    await db.refresh(db_user)
    return db_user