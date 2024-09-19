import requests
from requests import Response
from bs4 import BeautifulSoup
from starlette import status
from fastapi import HTTPException
from loguru import logger
from app.schemas.word_model import Word

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}


def _fetch_word_from_rae(name: str) -> tuple[Response, str]:
    base_url = "https://dle.rae.es/"
    final_url = f"{base_url}{name}"
    logger.info(f"Fetching URL: {final_url}")
    try:
        response = requests.get(final_url, headers=HEADERS)
        if response is None:
            raise ValueError("Received None from requests.get")
        response.raise_for_status()  # Lanza excepción para status code 4xx/5xx
        logger.info(f"Response status code: {response.status_code}")
        return response, final_url
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from RAE.")
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")



def _parse_response_into_word(response: Response, name: str, final_url: str) -> Word:
    status_code = response.status_code
    logger.info(f"The response status code of the word: {name} was {status_code}.")
    logger.info(f"Response content: {response.text[:500]}")  # Log the first 500 characters

    def get_definitions(s: BeautifulSoup) -> list[str]:
        defs = s.select('p.j')
        return [definition.get_text() for definition in defs]

    if status_code == status.HTTP_200_OK:
        try:
            soup = BeautifulSoup(response.text, features="html.parser")
            complete_name = soup.find("header").text
            definitions = get_definitions(s=soup)

            return Word(name=complete_name,
                        definitions=definitions,
                        url=final_url)
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error parsing the response.")
    elif status_code == status.HTTP_400_BAD_REQUEST:
        logger.error(f"Something went wrong for word {name}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There was an error in your request probably the word {name} does not exist.")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"There was an unexpected error.")



def fetch_word(name: str) -> Word:
    response, final_url = _fetch_word_from_rae(name)
    if response is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch word data.")
    return _parse_response_into_word(response=response, name=name, final_url=final_url)





