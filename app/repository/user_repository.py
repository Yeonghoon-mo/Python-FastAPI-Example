from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

# [Spring: @Repository]

# PK(Email)로 유저 조회
async def get_user(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

# 유저 생성 (BCrypt 적용)
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

# 유저 수정 (Update)
async def update_user(db: AsyncSession, db_user: User, user_update: UserUpdate):
    if user_update.password:
        db_user.password = get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
        
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 유저 삭제 (Delete)
async def delete_user(db: AsyncSession, db_user: User):
    await db.delete(db_user)
    await db.commit()
