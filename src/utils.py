import json
import logging
from pathlib import Path
from typing import Any

from src.external_api import TARGET_CURRENCY, convert_currency_at_rate

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Создание директории logs в корне проекта (на 2 уровня выше src/)
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Настроен file_handler для логера модуля utils
log_file_path = log_dir / "utils.log"
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настроен file_formatter для логера модуля utils
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
# Добавлен handler для логера модуля utils
logger.addHandler(file_handler)


def read_from_jsonfile(file_path: str) -> list[dict]:
    """
    Читает JSON-файл по указанному пути и возвращает список словарей.
    Если файл не найден, пустой или содержит не список, возвращает пустой
    список.
    """
    logger.debug(f"Начало загрузки транзакций из: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read().strip()

        if not data:
            raise ValueError("Файл пуст")

        transactions = json.loads(data)

        if not isinstance(transactions, list):
            raise TypeError

        logger.info(f"Успешно загружено {len(transactions)} транзакций")
        return transactions or []

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}")
        return []

    except TypeError:
        logger.warning("JSON содержит не список, возвращается пустой список")
        return []

    except ValueError as e:
        logger.error(f"Файл пустой или содержит ошибку структуры: {e}")
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
    logger.debug("Начало конвертации суммы транзакции")
    try:
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
            logger.info("Успешно получена сумма транзакции в рублях")
            return float(amount)

        # Поддерживаем только конвертацию из USD/EUR
        if currency not in ("USD", "EUR"):
            raise ValueError(
                f"Конвертация из валюты {currency} не поддерживается"
            )

        converted_amount = convert_currency_at_rate(
            amount, currency, TARGET_CURRENCY
        )

        logger.info(
            f"Успешно получена сумма транзакции в {TARGET_CURRENCY} из {currency}"
        )
        return round(converted_amount, 2)

    except ValueError as e:
        logger.error(f"Ошибка в транзакции: {e}")
        raise

    except Exception as e:
        logger.error(f"Непредвиденная ошибка при конвертации: {e}")
        raise
