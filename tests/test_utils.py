import json
from unittest.mock import Mock, patch

import pytest

from src.utils import convert_to_rubles, read_from_jsonfile


def test_valid_list_of_dicts(temp_json):
    """Валидный JSON-список словарей"""
    expected = [
        {"id": 1, "date": "2023-10-01", "amount": 5000.0},
        {"id": 2, "date": "2023-10-02", "amount": -120.5},
    ]
    temp_json.write_text(json.dumps(expected, ensure_ascii=False))
    assert read_from_jsonfile(str(temp_json)) == expected


def test_empty_file(temp_json):
    """Файл физически пуст"""
    temp_json.write_text("")
    assert read_from_jsonfile(str(temp_json)) == []


def test_whitespace_only_file(temp_json):
    """Файл содержит только пробелы/переносы"""
    temp_json.write_text("   \n\t  \n")
    assert read_from_jsonfile(str(temp_json)) == []


def test_json_not_a_list(temp_json):
    """JSON содержит объект, а не список"""
    temp_json.write_text('{"status": "ok", "count": 2}')
    assert read_from_jsonfile(str(temp_json)) == []


def test_invalid_json_syntax(temp_json):
    """Синтаксическая ошибка в JSON"""
    temp_json.write_text('{id: 1, "broken": true}')
    assert read_from_jsonfile(str(temp_json)) == []


def test_file_not_found():
    """Указанный путь не существует"""
    result = read_from_jsonfile("data/absolutely_missing.json")
    assert result == []


def test_convert_rub_no_api_call(make_transactions):
    """RUB не требует вызова API"""
    assert convert_to_rubles(make_transactions(1000, "RUB")) == 1000.0


@patch("src.external_api.requests.get")
def test_convert_usd_with_api(mock_get, make_transactions):
    """Конвертация USD через мок-ответ API"""
    # Настраиваем мок-ответ
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": "success",
        "conversion_result": 149632.2,
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_to_rubles(make_transactions(2000, "USD"))

    assert result == 149632.2
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_convert_eur_with_api(mock_get, make_transactions):
    """Конвертация EUR"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": "success",
        "conversion_result": 44119.6,
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    assert convert_to_rubles(make_transactions(500, "EUR")) == 44119.6


def test_unsupported_currency(make_transactions):
    """Неподдерживаемая валюта"""
    with pytest.raises(ValueError, match="не поддерживается"):
        convert_to_rubles(make_transactions(100, "GBP"))


def test_missing_amount(make_transactions_without_amount):
    """Отсутствует поле amount"""
    with pytest.raises(ValueError, match="не содержит поле 'amount'"):
        convert_to_rubles(make_transactions_without_amount("USD"))


@patch("src.external_api.requests.get")
def test_api_error_handling(mock_get, make_transactions):
    """Обработка ошибки API"""
    mock_get.side_effect = ConnectionError("Network error")

    with pytest.raises(ConnectionError):
        convert_to_rubles(make_transactions(100, "USD"))
