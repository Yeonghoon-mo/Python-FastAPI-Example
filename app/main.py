from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from contextlib import asynccontextmanager
from app.routers.v1 import auth_router, user_router, board_router, comment_router
from app.core.database import engine, Base
from app.core.logger import setup_logger
from app.core.config import settings
from app.core.redis import close_redis_connection
import os

# 로거 설정 초기화
logger = setup_logger()

# 비동기 DB 초기화 (Startup Event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: DB 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 업로드 디렉토리 생성
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    yield
    
    # Shutdown
    await close_redis_connection()

app = FastAPI(
    title="FastAPI Enterprise Architecture",
    description="Spring Boot의 견고한 구조를 이식한 엔터프라이즈급 FastAPI 보일러플레이트",
    version="0.0.1",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 실제 운영 환경에서는 허용할 도메인만 명시해야 해
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus 메트릭 설정 (Instrumentator)
Instrumentator().instrument(app).expose(app)

# 정적 파일 서버 설정 (프로필 이미지 등)
if not os.path.exists(settings.STATIC_DIR):
    os.makedirs(settings.STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# 라우터 등록 (v1)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(board_router, prefix="/api/v1")
app.include_router(comment_router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info("Root endpoint called!") # 색깔 있는 로그 출력!
    return {"message": "Hello World! FastAPI is running (Async Mode)! 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)