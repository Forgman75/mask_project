import logging
from typing import Any

import pandas as pd
import numpy as np


logger = logging.getLogger("files_reader")
logger.setLevel(logging.INFO)


def _normalize_row(row: dict[str, Any]) -> dict:
    """Приводит плоскую строку из CSV/XLSX к общей структуре транзакции."""
    amount = str(row.get("amount", "0") or "0")
    currency_name = str(row.get("currency_name", "") or "")
    currency_code = str(row.get("currency_code", "") or "")

    return {
        "id": int(row.get("id", 0) or 0),
        "state": str(row.get("state", "") or ""),
        "date": str(row.get("date", "") or ""),
        "description": str(row.get("description", "") or ""),
        "from": str(row.get("from", "") or ""),
        "to": str(row.get("to", "") or ""),
        "operationAmount": {
            "amount": amount,
            "currency": {
                "name": currency_name,
                "code": currency_code,
            },
        },
    }



def load_transactions_csv(
        file_path: str,
        sep: str = ",",
        encoding: str = "utf-8"
) -> list[dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.
    Возвращает список словарей с транзакциями.
    При ошибке или пустом файле возвращает пустой список.
    :param file_path: путь к CSV-файлу
    :param sep: разделитель (по умолчанию ',')
    :param encoding: кодировка файла (по умолчанию 'utf-8')
    """
    logger.debug(f"Начало чтения CSV-файла: {file_path}")
    try:
        df = pd.read_csv(file_path, encoding=encoding, sep=sep)
        if df.empty:
            logger.info("CSV-файл содержит только заголовки или пуст")
            return []
        logger.info(f"Успешно считано {len(df)} транзакций из CSV")
        # Исправлено: корректная замена NaN на None
        df = df.replace({np.nan: None, pd.NA: None})
        raw_records = df.to_dict(orient="records")
        return [_normalize_row(row) for row in raw_records]

    except FileNotFoundError:
        logger.error(f"CSV-файл не найден: {file_path}")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга структуры CSV: {e}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении CSV: {e}")
        return []


def load_transactions_excel(file_path: str) -> list[dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла (.xlsx/.xls).
    Возвращает список словарей с транзакциями.
    При ошибке или пустом файле возвращает пустой список.
    """
    logger.debug(f"Начало чтения Excel-файла: {file_path}")
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            logger.info("Excel-файл пуст или содержит только заголовки")
            return []
        logger.info(f"Успешно считано {len(df)} транзакций из Excel")
        df = df.replace({np.nan: None, pd.NA: None})
        raw_records = df.to_dict(orient="records")
        return [_normalize_row(row) for row in raw_records]
        
    except FileNotFoundError:
        logger.error(f"Excel-файл не найден: {file_path}")
        return []

    except ValueError as e:
        logger.error(f"Ошибка указания листа или формата Excel: {e}")
        return []

    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении Excel: {e}")
        return []
