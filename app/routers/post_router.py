from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services import post_service
from app.models.user import User

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# 글쓰기
@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_service.create_new_post(db=db, post=post, user_id=current_user.email)

# 목록 조회
@router.get("/", response_model=List[PostResponse])
def read_posts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return post_service.get_posts_list(db=db, skip=skip, limit=limit)

# 단건 조회
@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post_detail(db=db, post_id=post_id)

# 수정
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, 
    post_update: PostUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_service.update_existing_post(
        db=db, post_id=post_id, post_update=post_update, user_id=current_user.email
    )

# 삭제
@router.delete("/{post_id}")
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_service.delete_existing_post(db=db, post_id=post_id, user_id=current_user.email)
