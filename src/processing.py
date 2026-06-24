from operator import itemgetter
from collections import Counter
import re


def filter_by_state(
    in_list_dicts: list[dict], state: str | None = "EXECUTED"
) -> list[dict]:
    """
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    target = state.upper()
    return [
        item for item in in_list_dicts
        if str(item.get("state", "")).upper() == target
    ]


def sort_by_date(
    in_list_dicts: list[dict], reverse: bool = True
) -> list[dict]:
    """
    Функция должна возвращать новый список, отсортированный по дате
    (date). По умолчанию порядок сортировки обратный.
    """

    return sorted(in_list_dicts, key=itemgetter("date"), reverse=reverse)


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Подсчитывает количество банковских операций по категориям.
    Категория определяется значением поля description.
    Использует Counter из библиотеки collections.

    :param data: список словарей с данными о транзакциях
    :param categories: список названий категорий для подсчёта
    :return: словарь {категория: количество}
    """
    descriptions = [item.get("description", "") for item in data]
    counter = Counter(descriptions)
    return {category: counter.get(category, 0) for category in categories}


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список транзакций по строке поиска в поле description.
    Использует регулярные выражения (библиотека re) для поиска.
    Поиск регистронезависимый.

    :param data: список словарей с данными о транзакциях
    :param search: строка (или regex-паттерн) для поиска в описании
    :return: список словарей, у которых в description найдено совпадение
    """
    if not search:
        return list(data)

    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        # Если передан невалидный regex — ищем как обычную подстроку
        pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for item in data:
        description = item.get("description", "")
        if description and pattern.search(description):
            result.append(item)
    return result


