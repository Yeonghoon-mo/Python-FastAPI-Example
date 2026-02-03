import os
import uuid
from fastapi import UploadFile
from app.core.config import settings

class FileService:
    @staticmethod
    async def save_file(file: UploadFile, sub_dir: str = "") -> str:
        # 1. 파일 확장자 추출
        file_ext = os.path.splitext(file.filename)[1]
        
        # 2. 고유한 파일명 생성 (UUID)
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # 3. 저장 경로 설정
        upload_path = os.path.join(settings.UPLOAD_DIR, sub_dir)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, exist_ok=True)
            
        file_full_path = os.path.join(upload_path, unique_filename)
        
        # 4. 파일 저장
        with open(file_full_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # 5. 접근 가능한 URL 경로 반환
        return f"/static/uploads/{sub_dir}/{unique_filename}".replace("//", "/")

    @staticmethod
    def delete_file(file_path: str):
        if not file_path:
            return
            
        # URL 경로를 실제 파일 시스템 경로로 변환
        # 예: /static/uploads/profiles/xxx.jpg -> static/uploads/profiles/xxx.jpg
        actual_path = file_path.lstrip("/")
        if os.path.exists(actual_path):
            os.remove(actual_path)
