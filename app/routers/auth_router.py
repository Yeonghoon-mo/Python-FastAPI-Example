from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.token import Token
from app.services import auth_service, google_auth_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(tags=["authentication"])

# [로그인 API]
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.login(db=db, form_data=form_data)

# [Google 로그인 시작 API]
@router.get("/auth/google")
async def google_login():
    """Google 로그인 페이지로 리다이렉트"""
    auth_url = await google_auth_service.get_google_auth_url()
    return RedirectResponse(url=auth_url)

# [Google 로그인 콜백 API]
@router.get("/auth/google/callback", response_model=Token)
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Google 인증 후 자체 토큰 발급"""
    return await google_auth_service.authenticate_google_user(db=db, code=code)

# [로그아웃 API]
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return await auth_service.logout(email=current_user.email)
