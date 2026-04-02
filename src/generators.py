from typing import Iterator, Generator

def filter_by_currency(transactions: list[dict], currency: str) -> Iterator:
    def currency_filter(transaction):
        return transaction["operationAmount"]["currency"]["code"] == currency
    return filter(currency_filter, transactions)




def transaction_descriptions(transactions: list[dict]) -> Generator:
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")



def card_number_generator(start: int, stop: int) -> Generator:
     # Константы для валидации
    MIN_CARD_NUMBER = 1
    MAX_CARD_NUMBER = 9999999999999999  # 16 девяток
    
    # Валидация входных параметров
    if start < MIN_CARD_NUMBER:
        raise ValueError(
            f"Начальное значение должно быть >= {MIN_CARD_NUMBER}, "
            f"получено {start}"
        )
    
    if stop > MAX_CARD_NUMBER:
        raise ValueError(
            f"Конечное значение должно быть <= {MAX_CARD_NUMBER}, "
            f"получено {stop}"
        )
    
    if start > stop:
        raise ValueError(
            f"Начальное значение ({start}) не может быть больше "
            f"конечного ({stop})"
        )
    
    # Генерация номеров карт
    for number in range(start, stop + 1):  # +1 чтобы включить stop
        # Форматируем число в 16-значную строку с ведущими нулями
        card_number = f"{number:016d}"
        
        # Разбиваем на группы по 4 цифры с пробелами
        formatted = " ".join(
            card_number[i:i+4] for i in range(0, 16, 4)
        )
        
        yield formatted
