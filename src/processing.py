from operator import itemgetter


def filter_by_state(in_list_dicts: list[dict], state: str | None = "EXECUTED") -> list[dict]:
    """
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state
    соответствует указанному значению.
    """
    return [result_dict for result_dict in in_list_dicts if result_dict["state"] == state]


def sort_by_date(in_list_dicts: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция должна возвращать новый список, отсортированный по дате
    (date). По умолчанию порядок сортировки обратный.
    """

    return sorted(in_list_dicts, key=itemgetter("date"), reverse=reverse)
