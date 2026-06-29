from src.formatters import format_transaction


def test_format_transaction_with_from_and_to():
    tx = {
        "date": "2019-11-12T00:00:00",
        "description": "Перевод с карты на карту",
        "from": "MasterCard 1234567890123456",
        "to": "Visa Platinum 9876543210987654",
        "operationAmount": {"amount": "130.00", "currency": {"name": "USD"}},
    }
    result = format_transaction(tx)
    assert "12.11.2019 Перевод с карты на карту" in result
    assert (
        "MasterCard 1234 56** **** 3456 -> Visa Platinum 9876 54** **** 7654"
        in result
    )
    assert "Сумма: 130 USD" in result


def test_format_transaction_without_from():
    tx = {
        "date": "2019-12-08T00:00:00",
        "description": "Открытие вклада",
        "from": "",
        "to": "Счет 12345678901234567890",
        "operationAmount": {
            "amount": "40542.00",
            "currency": {"name": "руб."},
        },
    }
    result = format_transaction(tx)
    assert "08.12.2019 Открытие вклада" in result
    assert "Счет **7890" in result
    assert "->" not in result
    assert "Сумма: 40542 руб." in result


def test_format_transaction_missing_fields():
    tx = {}
    result = format_transaction(tx)
    assert "Сумма: 0" in result
