from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(info: str) -> str:
    """Функция для маскировки карт и счетов.
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

