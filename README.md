# 🚀 FastAPI + MariaDB CRUD Project

Spring Boot 개발자가 Python의 **FastAPI** 프레임워크를 학습하며 구현한 **RESTful API** 프로젝트입니다.
**Layered Architecture**를 적용하여 확장성과 유지보수성을 고려한 구조로 설계되었습니다.

---

## 🛠 Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI**: Modern, High-performance web framework
- **SQLAlchemy**: ORM (Object Relational Mapping)
- **Pydantic**: Data validation & settings management
- **Uvicorn**: ASGI Server

### Database
- **MariaDB** (MySQL Compatible)
- **PyMySQL**: Database Driver

### Security
- **JWT (JSON Web Token)**: Authentication
- **BCrypt**: Password Hashing (via Passlib)

---

## 📂 Project Structure (Layered Architecture)

Spring Boot의 계층형 아키텍처와 유사하게 구성하였습니다.

```text
app/
├── core/           # [Config] 설정, DB 연결, 로깅, 보안 관련 공통 로직
├── models/         # [Entity] DB 테이블 정의 (SQLAlchemy)
├── schemas/        # [DTO] 데이터 검증 및 응답 구조 (Pydantic)
├── repository/     # [Repository] DB 접근 로직 (CRUD)
├── services/       # [Service] 비즈니스 로직 (Transaction, Exception)
├── routers/        # [Controller] API 엔드포인트 정의
└── main.py         # [Application] 앱 진입점
```

---

## ✨ Features

### 1. User Management (CRUD)
- **Create**: 회원가입 (비밀번호 BCrypt 암호화)
- **Read**: 사용자 조회 (이메일 PK)
- **Update**: 정보 수정 (비밀번호, 활성 상태 등) - **[Auth Required]**
- **Delete**: 회원 탈퇴 - **[Auth Required]**

### 2. Authentication (보안)
- **Login**: JWT Access Token 발급 (`POST /token`)
- **Authorization**: `Bearer Token` 검증 미들웨어 구현
- **Permission**: 본인 계정만 수정/삭제 가능하도록 권한 체크 (`403 Forbidden`)

---

## 🚀 How to Run

### 1. 환경 변수 설정 (.env)
프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력하세요.

```ini
# Database
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=fastapi_db

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. 가상환경 생성 및 패키지 설치
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. 서버 실행
```bash
# 개발 모드 (Auto Reload)
uvicorn app.main:app --reload
```

### 4. API 문서 확인 (Swagger UI)
서버 실행 후 브라우저에서 접속:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Learning Points (Spring vs FastAPI)

| Concept | Spring Boot (Java) | FastAPI (Python) |
| :--- | :--- | :--- |
| **Controller** | `@RestController` | `APIRouter` |
| **Service** | `@Service` | `def service_func()` |
| **Repository** | `JpaRepository` | `Session.query(...)` |
| **DTO** | `Lombok @Data` | `Pydantic BaseModel` |
| **DI** | `@Autowired` | `Depends(...)` |
| **Config** | `application.yml` | `pydantic-settings (.env)` |

---

## 👨‍💻 Developer
- **Mo Yeonghoon**
- Backend Developer (Java/Kotlin, Python)
