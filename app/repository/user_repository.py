from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

# [Spring: @Repository]

# PK(Email)로 유저 조회
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 유저 생성 (BCrypt 적용)
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# 유저 수정 (Update)
def update_user(db: Session, db_user: User, user_update: UserUpdate):
    if user_update.password:
        db_user.password = get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
        
    db.commit()
    db.refresh(db_user)
    return db_user

# 유저 삭제 (Delete)
def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()