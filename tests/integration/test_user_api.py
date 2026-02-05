import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_api(client: AsyncClient):
    """사용자 회원가입 API 통합 테스트"""
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    # API 호출 (prefix /api/v1 추가)
    response = await client.post("/api/v1/users/", json=user_data)
    
    # 응답 검증
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["is_active"] is True

# Note: 소셜 로그인 전용 전환으로 인해 기존 /token API 테스트는 삭제되었습니다.
# 향후 소셜 로그인 Mock 테스트 등을 추가할 예정입니다.
