import json
from typing import Any

from src.external_api import TARGET_CURRENCY, convert_currency_at_rate


def read_from_jsonfile(file_path: str) -> list[dict]:
    """
    Читает JSON-файл по указанному пути и возвращает список словарей.
    Если файл не найден, пустой или содержит не список, возвращает пустой
    список.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)

        if not isinstance(transactions, list):
            raise TypeError

        return transactions or []

    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        # Файл не найден, содержит невалидный JSON или другую ошибку структуры
        return []


def convert_to_rubles(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции, ожидаются ключи:
            - amount: число (int/float)
            - currency: строка (RUB, USD, EUR)

    Returns:
        float: Сумма в рублях
    """
    amount = transaction.get("operationAmount", {}).get("amount")
    currency = (
        transaction.get("operationAmount", {})
        .get("currency", {})
        .get("code", "RUB")
    )

    if amount is None:
        raise ValueError("Транзакция не содержит поле 'amount'")

    # Если валюта уже в рублях — возвращаем как есть
    if currency == "RUB":
        return float(amount)

    # Поддерживаем только конвертацию из USD/EUR
    if currency not in ("USD", "EUR"):
        raise ValueError(f"Конвертация из валюты {currency} не поддерживается")

    converted_amount = convert_currency_at_rate(
        amount, currency, TARGET_CURRENCY
    )
    return round(converted_amount, 2)
