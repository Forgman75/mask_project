from operator import itemgetter


def filter_by_state(input_dict: list[dict], state: str | None = "EXECUTED") -> list[dict]:
    """
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state
    соответствует указанному значению.
    """
    return [result_dict for result_dict in input_dict if result_dict["state"] == state]


def sort_by_date(input_dict: list[dict], ascending: bool = True) -> list[dict]:
    """
    Функция должна возвращать новый список, отсортированный по дате
    (date).
    """

    return sorted(input_dict, key=itemgetter("date"), reverse=ascending)
