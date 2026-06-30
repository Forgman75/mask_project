import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


def test_filter_executed_state(mixed_state_operations: list[dict]) -> None:
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(mixed_state_operations, "EXECUTED")
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)
    assert [op["id"] for op in result] == [1, 4]


def test_filter_canceled_state(mixed_state_operations: list[dict]) -> None:
    """Тест фильтрации по статусу CANCELED"""
    result = filter_by_state(mixed_state_operations, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)


def test_filter_none_state(mixed_state_operations: list[dict]) -> None:
    """Тест фильтрации по None статусу"""
    result = filter_by_state(mixed_state_operations, None)

    # Ожидаем транзакции с пустым/отсутствующим state
    assert all(not item.get("state") for item in result)


def test_filter_nonexistent_state(mixed_state_operations: list[dict]) -> None:
    """Тест фильтрации по несуществующему статусу"""
    result = filter_by_state(mixed_state_operations, "UNKNOWN")
    assert result == []


def test_default_state_parameter(mixed_state_operations: list[dict]) -> None:
    """Тест значения параметра state по умолчанию (EXECUTED)"""
    result = filter_by_state(mixed_state_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_empty_list_filtering(empty_list: list) -> None:
    """Тест фильтрации пустого списка"""
    result = filter_by_state(empty_list, "EXECUTED")
    assert result == []


def test_filter_preserves_original_dicts(list_of_dicts: list[dict]) -> None:
    """Проверка что фильтрованные словари — те же объекты"""
    result = filter_by_state(list_of_dicts, "EXECUTED")
    assert result[0] is list_of_dicts[0]


def test_filter_by_status_case_insensitive(
    mixed_state_operations: list[dict],
) -> None:
    """Проверка что значение статуса не чувствительно к регистру"""
    result = filter_by_state(mixed_state_operations, "executed")
    assert len(result) == 2


@pytest.mark.parametrize(
    "state_value",
    [
        "EXECUTED",
        "CANCELED",
        "PENDING",
        "PROCESSING",
        "",
        None,
    ],
)
def test_parametrized_state_filtering(
    mixed_state_operations: list[dict], state_value: str | None
) -> None:
    """Параметризованный тест фильтрации разными статусами"""
    result = filter_by_state(mixed_state_operations, state_value)
    # Проверяем, что результат — список
    assert isinstance(result, list)
    # Проверяем, что все элементы имеют нужный state
    for item in result:
        if state_value is None:
            assert not item.get("state")
        else:
            assert str(item.get("state", "")).upper() == state_value.upper()


def test_missing_state_key_returns_empty() -> None:
    """Тест что отсутствие ключа 'state' возвращает пустой список"""
    data = [{"id": 1, "other": "value"}]
    result = filter_by_state(data, "EXECUTED")
    assert result == []


def test_sort_descending_default(unsorted_by_date: list[dict]) -> None:
    """Тест сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(unsorted_by_date)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)
    # Первый элемент — самая поздняя дата
    assert result[0]["id"] == 3  # 2024-06-20


def test_sort_ascending(unsorted_by_date: list[dict]) -> None:
    """Тест сортировки по возрастанию"""
    result = sort_by_date(unsorted_by_date, reverse=False)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates)
    # Первый элемент — самая ранняя дата
    assert result[0]["id"] in [2, 4]  # 2024-01-10


def test_stable_sort_same_dates(unsorted_by_date: list[dict]) -> None:
    """Тест стабильности сортировки при одинаковых датах"""
    result = sort_by_date(unsorted_by_date, reverse=False)
    # Находим элементы с одинаковой датой
    same_date_items = [
        op for op in result if op["date"] == "2024-01-10T08:00:00"
    ]
    # Проверяем что порядок относительно друг друга сохранён
    ids = [op["id"] for op in same_date_items]
    assert ids == [2, 4]


def test_empty_list_sorting(empty_list: list) -> None:
    """Тест сортировки пустого списка"""
    result = sort_by_date(empty_list)
    assert result == []


def test_single_element_list() -> None:
    """Тест сортировки списка из одного элемента"""
    data = [{"id": 1, "date": "2024-01-01T00:00:00"}]
    result = sort_by_date(data)
    assert result == data


def test_sort_preserves_original_dicts(unsorted_by_date: list[dict]) -> None:
    """Проверка что отсортированные словари — те же объекты"""
    result = sort_by_date(unsorted_by_date)
    assert all(orig in result for orig in unsorted_by_date)


def test_missing_date_key_raises_error() -> None:
    """Тест что отсутствие ключа 'date' вызывает ошибку"""
    data = [{"id": 1, "state": "EXECUTED"}]
    with pytest.raises((KeyError, TypeError)):
        sort_by_date(data)


@pytest.mark.parametrize(
    "reverse,expected_first_id",
    [
        (True, 3),  # Descending: 2024-06-20 first
        (False, 2),  # Ascending: 2024-01-10 first (id=2 или 4)
    ],
)
def test_parametrized_sort_order(
    unsorted_by_date: list[dict], reverse: bool, expected_first_id: int
) -> None:
    """Параметризованный тест порядка сортировки"""
    result = sort_by_date(unsorted_by_date, reverse=reverse)
    if reverse:
        assert result[0]["date"] >= result[-1]["date"]
    else:
        assert result[0]["date"] <= result[-1]["date"]


def test_process_bank_operations_basic(
    sample_transactions: list[dict],
) -> None:
    """Основной тест подсчета операций в каждой категории"""
    categories = [
        "Перевод с карты на карту",
        "Перевод организации",
        "Перевод со счета на счет",
    ]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {
        "Перевод с карты на карту": 1,
        "Перевод организации": 2,
        "Перевод со счета на счет": 2,
    }


def test_process_bank_operations_missing_category(
    sample_transactions: list[dict],
) -> None:
    """Тест с несуществующей категорией"""
    categories = ["Перевод организации", "Несуществующая"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {"Перевод организации": 2, "Несуществующая": 0}


def test_process_bank_operations_empty_data(empty_list: list) -> None:
    """Тест с попыткой подсчета операций по категории
      с пустым списком данных
    """
    categories = ["Перевод организации"]
    result = process_bank_operations(empty_list, categories)
    assert result == {"Перевод организации": 0}


def test_process_bank_operations_empty_categories(
    sample_transactions: list[dict],
) -> None:
    """Тест с попыткой подсчета операций с пустым списком категорий"""
    assert process_bank_operations(sample_transactions, []) == {}


def test_process_bank_operations_returns_dict(
    sample_transactions: list[dict],
) -> None:
    """Тест проверяющий что функция возвращает словарь"""
    result = process_bank_operations(
        sample_transactions, ["Перевод организации"]
    )
    assert isinstance(result, dict)


def test_process_bank_search_found(sample_data: list[dict]) -> None:
    """Тест нахождения совпадения в описании с поисковым словом"""
    result = process_bank_search(sample_data, "Открытие")
    assert len(result) == 2
    assert {item["id"] for item in result} == {1, 3}


def test_process_bank_search_not_found(sample_data: list[dict]) -> None:
    """Тест проверяющий случай, когда совпадения со словом нет"""
    result = process_bank_search(sample_data, "Пополнение")
    assert result == []


def test_process_bank_search_case_insensitive(sample_data: list[dict]) -> None:
    """Тест проверяющий регистронезависимость поискового слова"""
    result = process_bank_search(sample_data, "открытие")
    assert len(result) == 2


def test_process_bank_search_empty_data() -> None:
    """Тест проверяющий поиск на пустом списке"""
    assert process_bank_search([], "test") == []


def test_process_bank_search_empty_query(sample_data: list[dict]) -> None:
    """Тест проверяющий использование на данных пустого запроса"""
    assert process_bank_search(sample_data, "") == sample_data


def test_process_bank_search_regex(sample_data: list[dict]) -> None:
    """Тест проверяющий использование на данных regex-паттерна"""
    # Паттерн: слово, начинающееся на "Перевод" и заканчивающееся на "карты"
    result = process_bank_search(sample_data, r"Перевод.*карты")
    assert len(result) == 1
    assert result[0]["id"] == 4


def test_process_bank_search_missing_description() -> None:
    """Тест проверяющий поиск на данных с отсутствующим описанием"""
    data = [{"id": 1}, {"id": 2, "description": "Перевод"}]
    result = process_bank_search(data, "Перевод")
    assert len(result) == 1
    assert result[0]["id"] == 2
