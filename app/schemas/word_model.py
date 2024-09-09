from pydantic import BaseModel


class Word(BaseModel):
    name: str
    definition: list[str]
    url: str



