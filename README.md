🛡️ Bank Data Masking Utility
Утилита для маскировки банковских данных, форматирования дат и фильтрации финансовых операций.

📋 Описание
Этот скрипт предоставляет набор функций для безопасной обработки конфиденциальных финансовых данных:
* Маскировка номеров карт (первые 6 и последние 4 цифры)
* Маскировка номеров счетов (последние 4 цифры)
* Форматирование дат из ISO 8601 в читаемый формат
* Фильтрация операций по статусу
* Сортировка операций по дате
* Фильтрация транзакций по валюте
* Вывод описаний транзакций
* Генерация номеров карт
* Логирование

⚙️ Требования
Python 3.10+

 📥 Установка
1. Клонируйте репозиторий:
   ``` 
   git clone <repository-url>
   cd <project-folder>
   ```  
2. Создайте виртуальное окружение (рекомендуется):
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
🚀 Использование
Базовый пример
```
# Маскировка номера карты
card = get_mask_card_number(4587123456789012)
print(card)  # "458712******9012"

# Маскировка номера счёта
account = get_mask_account(12345678901234567890)
print(account)  # "**5678"

# Маскировка строки с типом и номером
info = mask_account_card("Visa 4587123456789012")
print(info)  # "Visa 458712******9012"

info = mask_account_card("Счет 12345678901234567890")
print(info)  # "Счет **5678"

# Форматирование даты
date = get_date("2024-03-15T10:30:00.123456")
print(date)  # "15.03.2024"

# Фильтрация операций
operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-15"},
    {"id": 2, "state": "CANCELED", "date": "2024-03-14"},
    {"id": 3, "state": "EXECUTED", "date": "2024-03-13"},
]
filtered = filter_by_state(operations, "EXECUTED")
print(filtered)  # [{"id": 1, ...}, {"id": 3, ...}]

# Сортировка операций по дате
sorted_ops = sort_by_date(operations, ascending=False)
print(sorted_ops)  # От новых к старым

# Поочередно выдает транзакции отфильтрованные по заданной валюте
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

>>> {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }

# Возвращает описание операции для каждой транзакции по очереди
descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

>>> Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации

# Генерирует номера карт в заданном диапазоне
for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005

# Декоратор для логирования результатов выполнения функции
>>> @log(filename="mylog.txt")
        ... def my_function(x, y):
        ...     return x + y
        >>> my_function(1, 2)
        3
        # В файл mylog.txt будет записано: "my_function ok"
        
        >>> @log()
        ... def another_function(x):
        ...     raise ValueError("Error")
        >>> another_function(1)
        # В консоль будет выведено: "another_function error: ValueError. Inputs: (1,), {}"
```
🧪 Тесты
```
# Запустить все тесты
pytest

# Запустить конкретный файл
pytest tests/test_masks.py

# Запустить конкретный тест
pytest tests/test_masks.py::test_valid_card_masking

# Запустить с отчётом о покрытии
pytest --cov=src --cov-report=term-missing

# Проверить что покрытие >= 80%
pytest --cov=src --cov-fail-under=80
```

📝 Лицензия
MIT License — свободное использование с указанием авторства.

