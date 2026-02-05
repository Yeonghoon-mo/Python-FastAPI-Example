from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services import comment_service
from app.models.user import User
from app.core.rate_limiter import RateLimiter

router = APIRouter(
    tags=["comments"],
)

# 댓글 작성
@router.post("/boards/{board_id}/comments", response_model=CommentResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_comment(
    board_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.create_new_comment(
        db=db, comment=comment, board_id=board_id, user_id=current_user.email
    )

# 특정 게시글의 댓글 목록 조회
@router.get("/boards/{board_id}/comments", response_model=List[CommentResponse])
async def read_comments(
    board_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await comment_service.get_comments_for_board(
        db=db, board_id=board_id, skip=skip, limit=limit
    )

# 댓글 수정
@router.put("/comments/{comment_id}", response_model=CommentResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.update_existing_comment(
        db=db, comment_id=comment_id, comment_update=comment_update, user_id=current_user.email
    )

# 댓글 삭제
@router.delete("/comments/{comment_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.delete_existing_comment(
        db=db, comment_id=comment_id, user_id=current_user.email
    )