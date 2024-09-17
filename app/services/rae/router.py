from venv import logger

from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.word_model import Word
from app.services.rae.get_word import fetch_word

rae_router: APIRouter = APIRouter(prefix="/rae", tags=["RAE"])


@rae_router.get("/word/")
def get_word(name: str) -> Word:
    """"
    Get a word of the RAE and return its definitions.
    """
    logger.info(f"Received request for word: {name}")
    return fetch_word(name=name)



