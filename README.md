🛡️ Bank Data Masking Utility
Утилита для маскировки банковских данных, форматирования дат и фильтрации финансовых операций.

📋 Описание
Этот скрипт предоставляет набор функций для безопасной обработки конфиденциальных финансовых данных:
* Маскировка номеров карт (первые 6 и последние 4 цифры)
* Маскировка номеров счетов (последние 4 цифры)
* Форматирование дат из ISO 8601 в читаемый формат
* Фильтрация операций по статусу
* Сортировка операций по дате

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
```

📝 Лицензия
MIT License — свободное использование с указанием авторства.

