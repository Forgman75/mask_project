from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Функция для маскировки карт и счетов.
    Она разделяет строку на части по пробелу.
    Получается две части: тип карты или счет, и номер карты или счета.
    По длине номера определяем, карта это или счет. Затем вызываем соответствующую
    функцию маскирования, соединяем результат с типом и возвращаем пользователю.

    """

    parts = info.split()

    card_or_account_type = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) == 16:
        masked_number = get_mask_card_number(int(number))
    elif len(number) == 20:
        masked_number = get_mask_account(int(number))
    else:
        raise ValueError("Некорректный номер карты или счета.")

    return f"{card_or_account_type} {masked_number}"


def get_date(date: str) -> str:
    """
    Функция для преобразования строки с датой в формате ISO 8601
    в строку вида "ДД.ММ.ГГГГ"
    """

    datetime_from_iso = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    result_date = datetime_from_iso.strftime("%d.%m.%Y")

    return result_date
