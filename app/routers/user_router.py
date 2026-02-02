from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, User, UserUpdate
from app.services import user_service
from app.models.user import User as UserModel # 타입 힌트용

# [Spring: @RestController]
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 회원가입 (누구나 가능)
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)

# 회원 조회 (누구나 가능 - 필요하면 보안 걸 수 있음)
@router.get("/{email}", response_model=User)
def read_user(email: str, db: Session = Depends(get_db)):
    return user_service.get_user(db=db, email=email)

# 회원 수정 (로그인 필수 + 본인만 가능)
@router.put("/{email}", response_model=User)
def update_user(
    email: str, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # [보안] 토큰 검증
):
    # 본인 확인 (Authorization)
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return user_service.update_user(db=db, email=email, user_update=user_update)

# 회원 삭제 (로그인 필수 + 본인만 가능)
@router.delete("/{email}")
def delete_user(
    email: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # [보안] 토큰 검증
):
    # 본인 확인 (Authorization)
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return user_service.delete_user(db=db, email=email)
