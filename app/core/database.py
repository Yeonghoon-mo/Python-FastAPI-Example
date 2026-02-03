from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# [Spring: DataSource] 비동기 커넥션 풀(Async Connection Pool) 생성
# echo=True: 실행되는 SQL을 콘솔에 출력 (Spring: spring.jpa.show-sql=true)
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL, 
    echo=True,
    # 비동기 처리를 위한 풀 사이즈 설정 등 추가 가능
    pool_size=10,
    max_overflow=20
)

# [Spring: EntityManagerFactory] 비동기 트랜잭션 관리 및 세션 생성 공장
# expire_on_commit=False: 비동기 환경에서 객체가 만료되지 않도록 설정 (필수)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# [JPA: @Entity가 상속받을 부모 클래스]
# 모든 모델(Entity)은 이 Base를 상속받아야 DB 테이블로 인식됩니다.
Base = declarative_base()

# [Spring: @Bean / DI] 의존성 주입(Dependency Injection)을 위한 함수
# Controller에서 db: AsyncSession = Depends(get_db) 로 주입받아 사용합니다.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
