from requests import Response
from bs4 import BeautifulSoup
from starlette import status
from fastapi import HTTPException, requests
from loguru import logger
from app.schemas.word_model import Word

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",

}


def _fetch_word_from_rae(name: str) -> tuple[Response, str]:
    base_url = "https://dle.rae.es/"
    final_url = base_url + name
    return requests.get(final_url, headers=HEADERS), final_url

def _parse_response_into_word(response: Response, name: str, final_url: str) -> Word:
    status_code = response.status_code
    logger.info(f"The response status code of the word: {name} was {status_code}.")

    def get_definitions(s: BeautifulSoup) -> list[str]: ...

    if status_code == status.HTTP_200_OK:
        soup = BeautifulSoup(response.text, features="html.parser")
        complete_name = soup.find("header").text
        definitions = get_definitions(s=soup)

        return Word(name=complete_name,
                    definitions=definitions,
                    url=final_url)

    elif status_code == status.HTTP_400_BAD_REQUEST:
        logger.error(f"Something went wrong for word {name}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There was an error in your request probably the word {name} does not exist.")

    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"There was an unexpected error.")

def fetch_word(name: str) -> Word:
    response, final_url = _fetch_word_from_rae(name)
    return _parse_response_into_word(response=response, name=name, final_url=final_url)


if __name__ == '__main__':
    word = get_word("pan")
    ...
