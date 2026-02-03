from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

async def get_comment(db: AsyncSession, comment_id: int):
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_comments_by_board(db: AsyncSession, board_id: int, skip: int = 0, limit: int = 100):
    stmt = select(Comment).where(Comment.board_id == board_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_comment(db: AsyncSession, comment: CommentCreate, board_id: int, user_id: str):
    db_comment = Comment(**comment.model_dump(), board_id=board_id, user_id=user_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def update_comment(db: AsyncSession, db_comment: Comment, comment_update: CommentUpdate):
    update_data = comment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(db: AsyncSession, db_comment: Comment):
    await db.delete(db_comment)
    await db.commit()