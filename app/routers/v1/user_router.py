from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, RoleChecker
from app.schemas.user import UserCreate, User, UserUpdate
from app.services import user_service
from app.services.file_service import FileService
from app.models.user import User as UserModel, UserRole # 타입 힌트 및 역할 Enum

# [Spring: @RestController]
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 권한 가드 정의
admin_only = RoleChecker([UserRole.ADMIN])

# 모든 유저 조회 (관리자 전용)
@router.get("/", response_model=list[User], dependencies=[Depends(admin_only)])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    """관리자만 모든 유저 목록을 볼 수 있습니다."""
    return await user_service.get_users(db=db)

# 프로필 이미지 업로드 (로그인 필수 + 본인만 가능)
@router.post("/{email}/profile-image", response_model=User)
async def upload_profile_image(
    email: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 본인 확인
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
    
    # 1. 기존 이미지가 있다면 삭제 (옵션: 필요 시)
    if current_user.profile_image_url:
        FileService.delete_file(current_user.profile_image_url)
    
    # 2. 새 이미지 저장
    image_url = await FileService.save_file(file, sub_dir="profiles")
    
    # 3. DB 업데이트
    return await user_service.update_profile_image(db=db, email=email, image_url=image_url)

# 회원가입 (누구나 가능)
@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db=db, user=user)

# 회원 조회 (누구나 가능 - 필요하면 보안 걸 수 있음)
@router.get("/{email}", response_model=User)
async def read_user(email: str, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user(db=db, email=email)

# 회원 수정 (로그인 필수 + 본인만 가능)
@router.put("/{email}", response_model=User)
async def update_user(
    email: str, 
    user_update: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # [보안] 토큰 검증
):
    # 본인 확인 (Authorization)
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return await user_service.update_user(db=db, email=email, user_update=user_update)

# 회원 삭제 (로그인 필수 + 본인만 가능)
@router.delete("/{email}")
async def delete_user(
    email: str, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # [보안] 토큰 검증
):
    # 본인 확인 (Authorization)
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return await user_service.delete_user(db=db, email=email)