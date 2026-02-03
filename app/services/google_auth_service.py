import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.config import settings
from app.core import security
from app.repository import user_repository
from app.models.user import User
from app.core.redis import redis_client

# [Spring: GoogleAuthService]

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

async def get_google_auth_url():
    """Google 로그인 페이지로 리다이렉트할 URL 생성"""
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{GOOGLE_AUTH_URL}?{query_string}"

async def authenticate_google_user(db: AsyncSession, code: str):
    """Google 인가 코드로 유저 정보를 가져와서 로그인 처리"""
    
    # 1. Authorization Code -> Access Token 교환
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
        )
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from Google"
            )
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        # 2. Access Token -> 유저 정보(Email, Name 등) 가져오기
        userinfo_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if userinfo_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
            
        user_info = userinfo_response.json()
        email = user_info.get("email")
        # social_id = user_info.get("sub") # Google의 고유 ID
        profile_image = user_info.get("picture")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )

        # 3. 우리 DB에 유저가 있는지 확인
        user = await user_repository.get_user(db, email=email)
        
        if not user:
            # 4. 없으면 신규 회원가입 (소셜 전용 유저)
            new_user = User(
                email=email,
                password=None, # 소셜 유저는 비번 없음
                provider="google",
                social_id=user_info.get("sub"),
                profile_image_url=profile_image,
                is_active=True
            )
            user = await user_repository.create_user(db, new_user)
        else:
            # 기존 유저라면 정보 업데이트 (선택 사항)
            user.provider = "google"
            user.social_id = user_info.get("sub")
            if profile_image:
                user.profile_image_url = profile_image
            await db.commit()
            await db.refresh(user)

        # 5. 자체 JWT 토큰 발급 (auth_service와 동일한 로직)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        our_access_token = security.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        # Redis에 세션 저장
        ttl_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        await redis_client.set(f"session:{user.email}", our_access_token, ex=ttl_seconds)
        
        return {"access_token": our_access_token, "token_type": "bearer"}
