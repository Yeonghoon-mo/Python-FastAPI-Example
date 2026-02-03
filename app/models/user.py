from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base

# [JPA: @Entity]
class User(Base):
    # [JPA: @Table(name = "users")]
    __tablename__ = "users"

    # [JPA: @Id]
    # 이메일을 PK로 사용합니다.
    email = Column(String(255), primary_key=True, index=True, nullable=False)

    # [JPA: @Column]
    # 소셜 로그인의 경우 비밀번호가 없을 수 있으므로 nullable=True로 변경
    password = Column(String(255), nullable=True)

    # 인증 제공자 (local, google, github 등)
    provider = Column(String(50), default="local", nullable=False)
    
    # 소셜 서비스에서 제공하는 고유 ID
    social_id = Column(String(255), nullable=True)

    # [JPA: @Column(columnDefinition = "TINYINT(1) default 1")]
    is_active = Column(Boolean, default=True)

    # 프로필 이미지 경로 저장
    profile_image_url = Column(String(500), nullable=True)

    # [JPA: @OneToMany(mappedBy = "owner")]
    boards = relationship("Board", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

    