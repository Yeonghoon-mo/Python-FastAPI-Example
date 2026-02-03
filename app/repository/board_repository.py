from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate

async def get_board(db: AsyncSession, board_id: int):
    stmt = select(Board).where(Board.id == board_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_boards(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Board).order_by(Board.id.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_boards_count(db: AsyncSession):
    stmt = select(func.count()).select_from(Board)
    result = await db.execute(stmt)
    return result.scalar()

async def create_board(db: AsyncSession, board: BoardCreate, user_id: str, image_url: str = None):
    db_board = Board(**board.model_dump(), user_id=user_id, image_url=image_url)
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    return db_board

async def update_board(db: AsyncSession, db_board: Board, board_update: BoardUpdate):
    update_data = board_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_board, key, value)
    
    await db.commit()
    await db.refresh(db_board)
    return db_board

async def delete_board(db: AsyncSession, db_board: Board):
    await db.delete(db_board)
    await db.commit()
