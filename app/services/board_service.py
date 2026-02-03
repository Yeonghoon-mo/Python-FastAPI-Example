from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repository import board_repository
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse
from app.services.file_service import FileService
from app.core.redis import redis_client
import json
import math
from app.schemas.page import PageResponse

async def create_new_board(db: AsyncSession, board: BoardCreate, user_id: str, image_url: str = None):
    # 캐시 무효화 (새 글 작성 시 목록 캐시 제거)
    await redis_client.delete("boards_page_1") # 단순 예시: 1페이지만 제거하거나 패턴 매칭으로 제거
    return await board_repository.create_board(db=db, board=board, user_id=user_id, image_url=image_url)

async def get_boards_list(db: AsyncSession, page: int = 1, size: int = 10):
    cache_key = f"boards_page_{page}_size_{size}"
    
    # 1. 캐시 조회
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return PageResponse(**json.loads(cached_data))

    # 2. DB 조회 (캐시 Miss)
    skip = (page - 1) * size

    db_items = await board_repository.get_boards(db=db, skip=skip, limit=size)
    total_count = await board_repository.get_boards_count(db=db)
    total_pages = math.ceil(total_count / size) if total_count > 0 else 0

    items_data = [BoardResponse.model_validate(item) for item in db_items]
    
    response = PageResponse(
        items=items_data,
        total_count=total_count,
        page=page,
        size=size,
        total_pages=total_pages
    )
    
    # 3. 캐시 저장 (TTL 60초)
    # Pydantic 모델을 JSON으로 직렬화
    await redis_client.set(cache_key, response.model_dump_json(), ex=60)
    
    return response

async def get_board_detail(db: AsyncSession, board_id: int):
    db_board = await board_repository.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

async def update_existing_board(db: AsyncSession, board_id: int, board_update: BoardUpdate, user_id: str, image_url: str = None):
    db_board = await get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this board")
    
    # 이미지 업데이트 시 기존 이미지 삭제
    if image_url:
        if db_board.image_url:
            FileService.delete_file(db_board.image_url)
        db_board.image_url = image_url
        
    return await board_repository.update_board(db=db, db_board=db_board, board_update=board_update)

async def delete_existing_board(db: AsyncSession, board_id: int, user_id: str):
    db_board = await get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
    
    # 게시글 삭제 시 첨부 이미지도 삭제
    if db_board.image_url:
        FileService.delete_file(db_board.image_url)
        
    await board_repository.delete_board(db=db, db_board=db_board)
    return {"message": "Board deleted successfully"}