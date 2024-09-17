from pydantic import BaseModel
from typing import List


class Word(BaseModel):
    name: str
    definition: list[str]
    url: str



