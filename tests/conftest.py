"""
Глобальные фикстуры и тестовые данные для всех тестов.
"""

import pytest


@pytest.fixture
def date_str_iso() -> str:
    """ISO-формат даты для тестов"""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def list_of_dicts() -> list[dict]:
    """Список словарей с операциями для тестов фильтрации и сортировки"""
    return [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
        },
    ]


@pytest.fixture
def list_of_payment() -> list[str]:
    """Список строк с картами и счетами для тестов маскировки"""
    return [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]


@pytest.fixture
def valid_card_numbers() -> list[int]:
    """Валидные номера карт (16 цифр)"""
    return [
        4587123456789012,
        5559123456789012,
        1234567890123456,
        9999888877776666,
    ]


@pytest.fixture
def valid_account_numbers() -> list[int]:
    """Валидные номера счетов (20 цифр)"""
    return [
        12345678901234567890,
        98765432109876543210,
        11112222333344445555,
    ]


@pytest.fixture
def expected_masked_cards() -> dict:
    """Ожидаемые результаты маскировки карт"""
    return {
        4587123456789012: "4587 12** **** 9012",
        5559123456789012: "5559 12** **** 9012",
        1234567890123456: "1234 56** **** 3456",
        9999888877776666: "9999 88** **** 6666",
    }


@pytest.fixture
def expected_masked_accounts() -> dict:
    """Ожидаемые результаты маскировки счетов"""
    return {
        12345678901234567890: "**7890",
        98765432109876543210: "**3210",
        11112222333344445555: "**5555",
    }


@pytest.fixture
def invalid_card_numbers() -> list[int]:
    """Невалидные номера карт (не 16 цифр)"""
    return [
        12345,  # Слишком короткий
        123456789012345,  # 15 цифр
        12345678901234567,  # 17 цифр
        0,  # Ноль
        -1234567890123456,  # Отрицательный
    ]


@pytest.fixture
def invalid_account_numbers() -> list[int]:
    """Невалидные номера счетов (не 20 цифр)"""
    return [
        1234567890,  # Слишком короткий
        1234567890123456789,  # 19 цифр
        123456789012345678901,  # 21 цифра
    ]


@pytest.fixture
def invalid_mask_inputs() -> list[str]:
    """Невалидные входные данные для mask_account_card"""
    return [
        "Invalid",  # Только тип, нет номера
        "1234567890123456",  # Только номер, нет типа
        "Card 12345",  # Номер неправильной длины
        "Счет 123",  # Счёт неправильной длины
        "",  # Пустая строка
        "  ",  # Только пробелы
        "Card 12345678901234567",  # 17 цифр (не карта и не счёт)
    ]


@pytest.fixture
def valid_iso_dates() -> list[str]:
    """Валидные даты в формате ISO 8601"""
    return [
        "2024-03-11T02:26:18.671407",
        "2019-07-03T18:35:29.512364",
        "2000-01-01T00:00:00.000000",
        "2024-12-31T23:59:59.999999",
    ]


@pytest.fixture
def expected_formatted_dates() -> dict:
    """Ожидаемые результаты форматирования дат"""
    return {
        "2024-03-11T02:26:18.671407": "11.03.2024",
        "2019-07-03T18:35:29.512364": "03.07.2019",
        "2000-01-01T00:00:00.000000": "01.01.2000",
        "2024-12-31T23:59:59.999999": "31.12.2024",
    }


@pytest.fixture
def invalid_date_formats() -> list[str]:
    """Невалидные форматы дат"""
    return [
        "2024-03-11",  # Без времени
        "11.03.2024",  # Неверный формат
        "2024/03/11T02:26:18",  # Другой разделитель
        "",  # Пустая строка
        "invalid",  # Полностью невалидная
        "2024-13-01T00:00:00",  # Неверный месяц
    ]


@pytest.fixture
def mixed_state_operations() -> list[dict]:
    """Операции с разными статусами для тестов фильтрации"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "PENDING", "date": "2024-01-02"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-03"},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-04"},
        {"id": 5, "state": None, "date": "2024-01-05"},
        {"id": 6, "state": "CANCELED", "date": "2024-01-06"},
    ]


@pytest.fixture
def unsorted_by_date() -> list[dict]:
    """Неотсортированный список операций для тестов сортировки"""
    return [
        {"id": 1, "date": "2024-03-15T10:00:00"},
        {"id": 2, "date": "2024-01-10T08:00:00"},
        {"id": 3, "date": "2024-06-20T15:00:00"},
        {"id": 4, "date": "2024-01-10T08:00:00"},  # Дубликат даты
        {"id": 5, "date": "2024-05-01T12:00:00"},
    ]


@pytest.fixture
def empty_list() -> list:
    """Пустой список для тестов граничных случаев"""
    return []


@pytest.fixture
def currency_codes():
    """Список кодов валют для параметризации"""
    return ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]


@pytest.fixture
def all_same_currency():
    """Все транзакции в одной валюте"""
    return [
        {
            "id": i,
            "operationAmount": {
                "amount": f"{i * 1000}.00",
                "currency": {"name": "USD", "code": "USD"}
            }
        }
        for i in range(1, 6)
    ]


@pytest.fixture
def single_usd_transaction():
    """Одна транзакция в USD"""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"}
            }
        }
    ]


@pytest.fixture
def malformed_transactions():
    """Транзакции с некорректной структурой"""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"}
            }
        },
        {
            "id": 2,
            # Отсутствует operationAmount
            "state": "EXECUTED"
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "3000.00",
                # Отсутствует currency
            }
        },
        {
            "id": 4,
            "operationAmount": {
                "amount": "4000.00",
                "currency": {
                    # Отсутствует code
                    "name": "RUB"
                }
            }
        },
        {
            "id": 5,
            "operationAmount": {
                "amount": "5000.00",
                "currency": {"name": "EUR", "code": "EUR"}
            }
        },
    ]


@pytest.fixture
def sample_transactions():
    """Фикстура для тестов генераторов"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def transaction_without_description():
    return [
        {"id": 1, "state": "EXECUTED"},
        {"description": "Перевод организации"},
    ]


@pytest.fixture
def expected_descriptions():
    """Ожидаемые из входных данных описания"""
    return [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ] 


@pytest.fixture
def valid_card_ranges():
    """Валидные диапазоны для генерации карт"""
    return [
        (1, 5),
        (1, 1),
        (100, 105),
        (1000, 1010),
        (10000, 10005),
    ]


@pytest.fixture
def expected_card_format():
    """Ожидаемый формат номера карты"""
    return "XXXX XXXX XXXX XXXX"


@pytest.fixture
def edge_case_ranges():
    """Граничные значения диапазонов"""
    return [
        (1, 1),  # Минимальное значение
        (9999999999999999, 9999999999999999),  # Максимальное значение
        (1, 10),  # Малый диапазон от минимума
        (9999999999999990, 9999999999999999),  # Малый диапазон у максимума
    ]


@pytest.fixture
def invalid_ranges():
    """Невалидные диапазоны для тестов ошибок"""
    return [
        (0, 5),  # start < 1
        (-10, 5),  # start отрицательный
        (1, 10000000000000000),  # stop > MAX
        (100, 50),  # start > stop
        (5, 5),  # Валидный случай (должен работать)
    ]
  
