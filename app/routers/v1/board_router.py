from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse
from app.schemas.page import PageResponse
from app.services import board_service
from app.services.file_service import FileService
from app.models.user import User
from app.core.rate_limiter import RateLimiter

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)

# 글쓰기 (Multipart/form-data)
@router.post("/", response_model=BoardResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_board(
    title: str = Form(...),
    content: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if file:
        image_url = await FileService.save_file(file, sub_dir="boards")
        
    board = BoardCreate(title=title, content=content)
    return await board_service.create_new_board(db=db, board=board, user_id=current_user.email, image_url=image_url)

# 수정 (Multipart/form-data)
@router.put("/{board_id}", response_model=BoardResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_board(
    board_id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if file:
        image_url = await FileService.save_file(file, sub_dir="boards")
    
    board_update = BoardUpdate(title=title, content=content)
    return await board_service.update_existing_board(
        db=db, board_id=board_id, board_update=board_update, user_id=current_user.email, image_url=image_url
    )

# 목록 조회 (Pagination 적용)
@router.get("/", response_model=PageResponse[BoardResponse])
async def read_boards(
    page: int = 1, 
    size: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    return await board_service.get_boards_list(db=db, page=page, size=size)

# 단건 조회
@router.get("/{board_id}", response_model=BoardResponse)
async def read_board(board_id: int, db: AsyncSession = Depends(get_db)):
    return await board_service.get_board_detail(db=db, board_id=board_id)

# 삭제
@router.delete("/{board_id}", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def delete_board(
    board_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await board_service.delete_existing_board(db=db, board_id=board_id, user_id=current_user.email)
