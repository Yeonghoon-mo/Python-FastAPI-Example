import logging
import sys
from loguru import logger

class InterceptHandler(logging.Handler):
    """
    Python 표준 logging 모듈의 로그를 Loguru로 가로채는 핸들러
    """
    def emit(self, record):
        # Loguru의 레벨로 매핑
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 호출 스택 깊이 찾기
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logger():
    # 1. Uvicorn의 기본 로그 핸들러들을 싹 제거 (우리가 접수한다! 😎)
    logging.getLogger("uvicorn").handlers = []
    logging.getLogger("uvicorn.access").handlers = []
    
    # 2. 모든 표준 로거가 InterceptHandler를 거치도록 설정
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # 3. Loguru 설정 (기존과 동일)
    logger.remove()
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 콘솔 출력
    logger.add(sys.stderr, format=log_format, level="INFO")

    return logger