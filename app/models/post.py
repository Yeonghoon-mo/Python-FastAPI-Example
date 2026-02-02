from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# [JPA: @Entity]
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    
    # [JPA: @ManyToOne]
    # user_id는 users 테이블의 email 컬럼을 참조합니다.
    user_id = Column(String(255), ForeignKey("users.email"))
    
    # [JPA: @CreatedDate / @LastModifiedDate]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # [JPA: 양방향 매핑]
    # User 모델에서 back_populates로 연결됩니다.
    owner = relationship("User", back_populates="posts")
