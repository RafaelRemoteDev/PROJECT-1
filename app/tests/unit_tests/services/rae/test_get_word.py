from app.services.rae.get_word import _parse_response_into_word
from unittest.mock import Mock

def test_parse_response_into_word():
    mock_response = Mock(spec=Response)
    mock_response.text = ...
    _parse_response_into_word(response=...)

