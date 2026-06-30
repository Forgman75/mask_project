import sys

from src.files_reader import load_transactions_csv, load_transactions_excel
from src.formatters import format_transaction
from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import read_from_jsonfile

YES_ANSWERS = {"да", "yes", "y", "yep", "true", "1"}
NO_ANSWERS = {"нет", "no", "n", "nope", "false", "0"}
VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
EXIT_COMMANDS = {"exit", "выход", "quit", "q", "0"}


def _is_exit_command(value: str) -> bool:
    """Проверяет, является ли введённое значение командой выхода."""
    return value.strip().lower() in EXIT_COMMANDS


def _ask_yes_no(prompt: str) -> bool | None:
    """
    Спрашивает пользователя Да/Нет.
    Возвращает:
      - True  — если ответ положительный
      - False — если ответ отрицательный
      - None  — если введена команда выхода
    """

    while True:
        answer = input(prompt).strip().lower()
        if _is_exit_command(answer):
            return None
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'." "(или 'exit' для выхода).")


def _choose_file_type() -> str | None:
    """
    Запрашивает тип файла.
    Возвращает '1', '2', '3' или None (если команда выхода).
    """

    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакций из XLSX-файла")
    print("(Для выхода введите 'exit')")
    while True:
        choice = input().strip()
        if _is_exit_command(choice):
            return None
        if choice in {"1", "2", "3"}:
            return choice
        print("Неверный ввод. Введите 1, 2 или 3. (или 'exit' для выхода).")


def _ask_file_path() -> str | None:
    """
    Запрашивает путь к файлу.
    Возвращает путь или None (если команда выхода).
    """
    while True:
        filepath = input(
            "Введите путь к файлу (или 'exit' для выхода): "
        ).strip()
        if _is_exit_command(filepath):
            return None
        if filepath:
            return filepath
        print("Путь не может быть пустым. Попробуйте ещё раз.")


def _ask_status() -> str | None:
    """
    Запрашивает статус для фильтрации.
    Возвращает статус или None (если команда выхода).
    """
    while True:
        print(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            "(Для выхода введите 'exit')"
        )
        status = input().strip().upper()
        if _is_exit_command(status):
            return None
        if status in VALID_STATUSES:
            return status
        print(f'Статус операции "{status}" недоступен.')


def _ask_sort_direction() -> bool | None:
    """
    Запрашивает направление сортировки.
    Возвращает:
      - True  — сортировка по убыванию
      - False — сортировка по возрастанию
      - None  — если команда выхода
    """
    while True:
        direction = (
            input("Отсортировать по возрастанию или по убыванию? ")
            .strip()
            .lower()
        )
        if _is_exit_command(direction):
            return None
        if "возраст" in direction:
            return False
        if "убыв" in direction:
            return True
        print(
            "Пожалуйста, введите 'по возрастанию' или"
            " 'по убыванию' (или 'exit' для выхода)."
        )


def _ask_search_word() -> str | None:
    """
    Запрашивает слово для поиска в описании.
    Возвращает слово или None (если команда выхода).
    """
    while True:
        word = input(
            "Введите слово для поиска (или 'exit' для выхода): "
        ).strip()
        if _is_exit_command(word):
            return None
        if word:
            return word
        print("Слово не может быть пустым. Попробуйте ещё раз.")


def _load_file(choice: str, filepath: str) -> list:
    """Загружает данные из файла выбранного типа."""
    if choice == "1":
        return read_from_jsonfile(filepath)
    elif choice == "2":
        return load_transactions_csv(filepath, sep=";")
    else:
        return load_transactions_excel(filepath)


def main():
    print(
        "Привет! Добро пожаловать в программу работы с" \
        " банковскими транзакциями."
    )
    print(
        "Подсказка: на любом шаге вы можете ввести 'exit'"
        "или 'выход' для завершения программы.\n"
    )

    # 1. Выбор типа файла
    choice = _choose_file_type()
    if choice is None:
        _goodbye()
        return

    file_type = {"1": "JSON", "2": "CSV", "3": "XLSX"}[choice]
    print(f"Для обработки выбран {file_type}-файл.")

    data = None
    while data is None:
        filepath = _ask_file_path()
        if filepath is None:
            _goodbye()
            return

        try:
            data = _load_file(choice, filepath)
            print(f"Файл '{filepath}' успешно загружен.")
        except FileNotFoundError:
            print(f"Файл не найден: {filepath}")
            print("   Проверьте путь и попробуйте снова.\n")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            print("   Попробуйте ввести путь ещё раз.\n")

    # 2. Фильтрация по статусу
    status = _ask_status()
    if status is None:
        _goodbye()
        return

    print(f'Операции отфильтрованы по статусу "{status}"')
    data = filter_by_state(data, status)

    # 3. Сортировка по дате
    sort_choice = _ask_yes_no("\nОтсортировать операции по дате? Да/Нет\n")
    if sort_choice is None:
        _goodbye()
        return
    if sort_choice:
        direction = _ask_sort_direction()
        if direction is None:
            _goodbye()
            return
        data = sort_by_date(data, reverse=direction)

    # 4. Только рублёвые транзакции
    rub_only = _ask_yes_no("\nВыводить только рублевые транзакции? Да/Нет\n")
    if rub_only is None:
        _goodbye()
        return
    if rub_only:
        data = list(filter_by_currency(data, "RUB"))

    # 5. Поиск по слову в описании
    search_choice = _ask_yes_no(
        "\nОтфильтровать список транзакций по определенному слову в описании?"
        "Да/Нет\n"
    )
    if search_choice is None:
        _goodbye()
        return
    if search_choice:
        search_word = _ask_search_word()
        if search_word is None:
            _goodbye()
            return
        data = process_bank_search(data, search_word)

    # 6. Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not data:
        print(
            "\nНе найдено ни одной транзакции," \
            " подходящей под ваши условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}\n")
    for tx in data:
        print(format_transaction(tx))
        print()


def _goodbye():
    """Выводит прощальное сообщение."""
    print("\n👋 Спасибо за использование программы. До свидания!")


if __name__ == "__main__":
    main()
