from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, User
from app.repository import user_repository

# Spring의 @RequestMapping("/users") 역할
router = APIRouter(
    prefix="/users",
    tags=["users"],  # Swagger에서 그룹화할 태그
)

# 회원가입 (POST /users)
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 중복 이메일 체크
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_repository.create_user(db=db, user=user)

# 회원 조회 (GET /users/{user_id})
@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user
