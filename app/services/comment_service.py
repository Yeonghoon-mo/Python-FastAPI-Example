from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repository import comment_repository, board_repository
from app.schemas.comment import CommentCreate, CommentUpdate

async def create_new_comment(db: AsyncSession, comment: CommentCreate, board_id: int, user_id: str):
    # 게시글 존재 확인
    db_board = await board_repository.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    
    return await comment_repository.create_comment(db=db, comment=comment, board_id=board_id, user_id=user_id)

async def get_comments_for_board(db: AsyncSession, board_id: int, skip: int = 0, limit: int = 100):
    # 게시글 존재 확인
    db_board = await board_repository.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
        
    return await comment_repository.get_comments_by_board(db=db, board_id=board_id, skip=skip, limit=limit)

async def update_existing_comment(db: AsyncSession, comment_id: int, comment_update: CommentUpdate, user_id: str):
    db_comment = await comment_repository.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # 본인 확인
    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
    return await comment_repository.update_comment(db=db, db_comment=db_comment, comment_update=comment_update)

async def delete_existing_comment(db: AsyncSession, comment_id: int, user_id: str):
    db_comment = await comment_repository.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # 본인 확인
    if db_comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
        
    await comment_repository.delete_comment(db=db, db_comment=db_comment)
    return {"message": "Comment deleted successfully"}