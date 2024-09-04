from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum


class WordType(Enum):
    VERB = "Verb"
    SUBSTANTIVE = "Substantive"


class Word(BaseModel, ABC):
    word: str
    definition: str
    enlace: str
    word_type: WordType

    @abstractmethod
    def validate_word_type(self) -> bool:
        ...


class Verb(Word):
    def validate_word_type(self) -> bool:
        return self.word.endswith("er") or self.word.endswith("ar") or self.word.endswith("ir")


class Substantive(Word):
    def validate_word_type(self):
        return True
