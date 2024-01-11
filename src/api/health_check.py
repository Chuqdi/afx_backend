import datetime
from src.utils.logger import get_logger
from fastapi import APIRouter, status

router = APIRouter()
logger = get_logger("MAIN")


@router.get("/")
async def health_check():
    return {
        "ping": "PONG",
        "status": status.HTTP_200_OK,
        "date": datetime.datetime.now(),
    }
