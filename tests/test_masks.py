import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number,expected",
    [
        (4587123456789012, "4587 12** **** 9012"),
        (5559123456789012, "5559 12** **** 9012"),
        (1234567890123456, "1234 56** **** 3456"),
        (9999888877776666, "9999 88** **** 6666"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_valid_card_masking(card_number: int, expected: str) -> None:
    """Тест маскировки валидных номеров карт"""
    result = get_mask_card_number(card_number)
    assert result == expected
    assert len(result) == 19
    assert result.count("*") == 6


@pytest.mark.parametrize(
    "card_number",
    [
        12345,  # Слишком короткий
        123456789012345,  # 15 цифр
        12345678901234567,  # 17 цифр
        0,  # Ноль
        -1234567890123456,  # Отрицательный
    ],
)
def test_invalid_card_length(card_number: int) -> None:
    """Тест обработки карт неправильной длины.
    Функция должна работать, но результат может быть некорректным.
    Проверяем что не падает с исключением"""
    result = get_mask_card_number(card_number)
    assert isinstance(result, str)
    assert len(result) > 0


def test_card_masking_preserves_first_and_last() -> None:
    """Проверка что первые 6 и последние 4 цифры сохраняются"""
    card = 4587123456789012
    card_str = str(card)
    result = get_mask_card_number(card)
    # Удаляем пробелы и звёздочки для проверки
    cleaned = result.replace(" ", "").replace("*", "")
    assert cleaned.startswith(card_str[:6])
    assert cleaned.endswith(card_str[-4:])


def test_card_masking_format() -> None:
    """Проверка формата вывода: группы по 4 цифры с пробелами"""
    result = get_mask_card_number(4587123456789012)
    parts = result.split()
    assert len(parts) == 4  # 4 группы
    assert all(len(part) == 4 for part in parts)  # Каждая по 4 символа


@pytest.mark.parametrize(
    "account_number,expected",
    [
        (12345678901234567890, "**7890"),
        (98765432109876543210, "**3210"),
        (11112222333344445555, "**5555"),
        (10000000000000000001, "**0001"),
    ],
)
def test_valid_account_masking(account_number: int, expected: str) -> None:
    """Тест маскировки валидных номеров счетов"""
    result = get_mask_account(account_number)
    assert result == expected
    assert result.startswith("**")
    assert len(result) == 6  # "**" + 4 цифры


@pytest.mark.parametrize(
    "account_number",
    [
        1234567890,  # Слишком короткий
        1234567890123456789,  # 19 цифр
        123456789012345678901,  # 21 цифра
        0,  # Ноль
    ],
)
def test_invalid_account_length(account_number: int) -> None:
    """Тест обработки счетов неправильной длины"""
    result = get_mask_account(account_number)
    assert isinstance(result, str)
    assert result.startswith("**")
    # Проверяем что последние 4 цифры (или меньше) присутствуют
    account_str = str(abs(account_number))
    expected_suffix = (
        account_str[-4:] if len(account_str) >= 4 else account_str
    )
    assert result.endswith(expected_suffix)


def test_account_masking_preserves_last_four() -> None:
    """Проверка что последние 4 цифры сохраняются"""
    account = 12345678901234567890
    account_str = str(account)
    result = get_mask_account(account)

    assert result.endswith(account_str[-4:])
    assert result[:2] == "**"


def test_account_masking_short_number() -> None:
    """Тест маскировки очень короткого номера"""
    result = get_mask_account(123)
    assert result == "**123"  # Все цифры сохраняются если их < 4


def test_card_with_zeros() -> None:
    """Тест карты с нулями в разных позициях"""
    result = get_mask_card_number(1000000000000001)
    assert "1000 00** **** 0001" == result


def test_account_with_zeros() -> None:
    """Тест счёта с нулями"""
    result = get_mask_account(10000000000000000001)
    assert result == "**0001"


def test_maximum_card_number() -> None:
    """Тест максимального 16-значного числа"""
    result = get_mask_card_number(9999999999999999)
    assert result == "9999 99** **** 9999"


def test_minimum_valid_card() -> None:
    """Тест минимального 16-значного числа"""
    result = get_mask_card_number(1000000000000000)
    assert result == "1000 00** **** 0000"


def test_type_error_on_string_input() -> None:
    """Тест что функция ожидает int, а не str"""
    with pytest.raises((TypeError, AttributeError)):
        # Если передать строку, str() сработает, но это не по контракту
        # Проверяем поведение
        result = get_mask_card_number("4587123456789012")
        assert isinstance(result, str)
