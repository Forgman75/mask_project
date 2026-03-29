import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        (
            "Visa Platinum 8990922113665229",
            "Visa Platinum 8990 92** **** 5229",
        ),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ],
)
def test_card_masking_various_types(input_str: str, expected: str) -> None:
    """Тест маскировки карт разных типов"""
    result = mask_account_card(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Account 12345678901234567890", "Account **7890"),
    ],
)
def test_account_masking_various_types(input_str: str, expected: str) -> None:
    """Тест маскировки счетов с разными префиксами"""
    result = mask_account_card(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "Invalid",  # Только тип
        "1234567890123456",  # Только номер
        "Card 12345",  # Неправильная длина
        "Счет 123",  # Неправильная длина
        "",  # Пустая строка
        "  ",  # Только пробелы
        "Card 12345678901234567",  # 17 цифр
        "Card 123456789012345",  # 15 цифр
    ],
)
def test_invalid_inputs_raise_error(invalid_input: str) -> None:
    """Тест обработки невалидных входных данных"""
    with pytest.raises((ValueError, IndexError)):
        mask_account_card(invalid_input)


def test_multi_word_card_type() -> None:
    """Тест типа карты из нескольких слов"""
    result = mask_account_card("Visa Platinum Gold 1234567890123456")
    assert result.startswith("Visa Platinum Gold")
    assert "1234 56** **** 3456" in result


def test_preserves_original_type_name() -> None:
    """Проверка что имя типа сохраняется без изменений"""
    input_str = "МИР карта 1234567890123456"
    result = mask_account_card(input_str)
    assert result.startswith("МИР карта")


def test_whitespace_handling() -> None:
    """Тест обработки лишних пробелов"""
    # Функция использует split(), поэтому множественные пробелы схлопываются
    result = mask_account_card("Visa    1234567890123456")
    assert "Visa" in result
    assert "1234 56** **** 3456" in result


@pytest.mark.parametrize(
    "iso_date,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        ("2024-12-31T23:59:59.999999", "31.12.2024"),
        ("2024-06-15T12:30:45.123456", "15.06.2024"),
    ],
)
def test_valid_iso_date_conversion(iso_date: str, expected: str) -> None:
    """Тест конвертации валидных дат из ISO в формат ДД.ММ.ГГГГ"""
    result = get_date(iso_date)
    assert result == expected
    # Проверяем формат: ДД.ММ.ГГГГ
    assert len(result) == 10
    assert result[2] == "." and result[5] == "."


@pytest.mark.parametrize(
    "invalid_date",
    [
        "2024-03-11",  # Без времени
        "11.03.2024",  # Неверный формат
        "2024/03/11T02:26:18",  # Другой разделитель
        "",  # Пустая строка
        "invalid",  # Полностью невалидная
        "2024-13-01T00:00:00",  # Неверный месяц
        "2024-02-30T00:00:00",  # Неверный день
    ],
)
def test_invalid_date_formats(invalid_date: str) -> None:
    """Тест обработки невалидных форматов дат"""
    with pytest.raises((ValueError, IndexError)):
        get_date(invalid_date)


def test_date_ignores_time_component() -> None:
    """Проверка что время не влияет на результат"""
    date1 = "2024-03-11T00:00:00.000000"
    date2 = "2024-03-11T23:59:59.999999"
    assert get_date(date1) == get_date(date2) == "11.03.2024"


def test_leap_year_date() -> None:
    """Тест даты 29 февраля високосного года"""
    result = get_date("2024-02-29T12:00:00.000000")
    assert result == "29.02.2024"


def test_millisecond_precision_ignored() -> None:
    """Проверка что миллисекунды игнорируются"""
    dates = [
        "2024-03-11T12:00:00.000000",
        "2024-03-11T12:00:00.123456",
        "2024-03-11T12:00:00.999999",
    ]
    results = [get_date(d) for d in dates]
    assert all(r == "11.03.2024" for r in results)
