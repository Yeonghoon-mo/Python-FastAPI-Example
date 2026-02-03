import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_api(client: AsyncClient):
    """사용자 회원가입 API 통합 테스트"""
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    # API 호출
    response = await client.post("/users/", json=user_data)
    
    # 응답 검증
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["is_active"] is True

@pytest.mark.asyncio
async def test_login_api(client: AsyncClient):
    """로그인 및 JWT 토큰 발급 테스트"""
    # 1. 먼저 회원가입
    user_data = {
        "email": "login_test@example.com",
        "password": "password123"
    }
    await client.post("/users/", json=user_data)
    
    # 2. 로그인 시도
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = await client.post("/token", data=login_data)
    
    # 3. 검증
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
