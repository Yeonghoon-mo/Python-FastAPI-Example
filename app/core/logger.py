import sys
from loguru import logger

def setup_logger():
    # 기존 로그 핸들러 제거 (중복 출력 방지)
    logger.remove()

    # 콘솔 로그 포맷 설정 (색상 및 구분)
    # <green>{time}</green>: 시간 (초록색)
    # <level>{level: <8}</level>: 로그 레벨 (INFO, ERROR 등) - 레벨별 자동 색상 적용
    # <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>: 파일명:함수:라인 (하늘색)
    # <level>{message}</level>: 메시지
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 1. 콘솔 출력 (Stderr)
    logger.add(sys.stderr, format=log_format, level="INFO")

    # 2. 파일 저장 (선택 사항 - logs 폴더에 날짜별로 저장)
    # logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="500 MB", level="DEBUG")

    return logger
