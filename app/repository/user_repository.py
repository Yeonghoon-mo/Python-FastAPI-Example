from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


# ID 로 유저 조회
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# 이메일로 유저 조회 (중복 가입 체크용)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# 유저 생성
def create_user(db: Session, user: UserCreate):
    # TODO bcrypt로 교체 예정.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)

    db.add(db_user)  # 영속성 컨텍스트에 담기 (Staging)
    db.commit()  # DB에 반영
    db.refresh(db_user)  # DB에서 생성된 ID 등 최신 정보 가져오기
    return db_user
