from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date, process_bank_search
from src.utils import read_from_jsonfile
from src.formatters import format_transaction
from src.files_reader import load_transactions_csv, load_transactions_excel


YES_ANSWERS = {"да", "yes", "y", "yep", "true", "1"}
NO_ANSWERS = {"нет", "no", "n", "nope", "false", "0"}
VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _ask_yes_no(prompt: str) -> bool | None:
    """Спрашивает пользователя Да/Нет. Возвращает True/False/None (если не понял)."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'.")


def _choose_file_type() -> str:
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакций из XLSX-файла")
    while True:
        choice = input().strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Неверный ввод. Введите 1, 2 или 3.")


def _ask_status() -> str:
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status = input().strip().upper()
        if status in VALID_STATUSES:
            return status
        print(f'Статус операции "{status}" недоступен.')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Выбор типа файла
    choice = _choose_file_type()
    file_type = {"1": "JSON", "2": "CSV", "3": "XLSX"}[choice]
    print(f"Для обработки выбран {file_type}-файл.")

    filepath = input("Введите путь к файлу: ").strip()
    try:
        if choice == "1":
            data = read_from_jsonfile(filepath)
        elif choice == "2":
            data = load_transactions_csv(filepath, sep=';')
        else:
            data = load_transactions_excel(filepath)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # 2. Фильтрация по статусу
    status = _ask_status()
    print(f'Операции отфильтрованы по статусу "{status}"')
    data = filter_by_state(data, status)

    # 3. Сортировка по дате
    if _ask_yes_no("Отсортировать операции по дате? Да/Нет\n"):
        direction = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = "убыв" in direction
        data = sort_by_date(data, reverse=reverse)

    # 4. Только рублёвые транзакции
    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет\n"):
        data = filter_by_currency(data, "RUB")

    # 5. Поиск по слову в описании
    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        search_word = input("Введите слово для поиска: ").strip()
        data = process_bank_search(data, search_word)

    # 6. Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not data:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}\n")
    for tx in data:
        print(format_transaction(tx))
        print()

    
if __name__ == "__main__":
    main()
