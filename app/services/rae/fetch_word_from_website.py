import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from requests import Response
from starlette import status
from loguru import logger

from app.schemas.word_model import WordModel

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36 [ip:5.91.168.176]"
}


def _fetch_word_from_rae(name: str) -> tuple[Response, str]:
    base_url = "https://dle.rae.es/"
    final_url = base_url + name
    return requests.get(final_url, headers=HEADERS), final_url


def parse_response_into_word(response: Response, name: str, final_url: str) -> WordModel:
    status_code = response.status_code
    logger.info(f"The response status code of the word: {name} was {status_code}.")

    def get_definitions(s: BeautifulSoup) -> list[str]:
        defs = s.select('p[class^="j"]')
        return [definition.get_text() for definition in defs]

    if status_code == status.HTTP_200_OK:
        soup = BeautifulSoup(response.text, features="html.parser")
        if (header := soup.find("header")) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The word '{name}' has not been found.")

        complete_name = header.text
        definitions = get_definitions(s=soup)

        return WordModel(name=complete_name,
                         definitions=definitions,
                         url=final_url)

    elif status_code == status.HTTP_400_BAD_REQUEST:
        logger.error(f"Error for word: {name}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There was an error in your request probably the word '{name}' does not exist.")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"There was an unexpected error.")


def fetch_word_from_website(name: str) -> WordModel:
    response, final_url = _fetch_word_from_rae(name)
    return parse_response_into_word(response=response, name=name, final_url=final_url)






