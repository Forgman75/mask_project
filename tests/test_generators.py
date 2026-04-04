import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions
)


def test_filter_usd_transactions(sample_transactions: list[dict]) -> None:
    """Тест фильтрации транзакций в USD"""
    result = list(filter_by_currency(sample_transactions, "USD"))

    assert len(result) == 3
    assert all(
        t["operationAmount"]["currency"]["code"] == "USD" for t in result
    )
    assert [t["id"] for t in result] == [939719570, 142264268, 895315941]


def test_returns_iterator_type(sample_transactions: list[dict]) -> None:
    """Тест что функция возвращает итератор"""
    result = filter_by_currency(sample_transactions, "USD")

    # Проверяем что это итератор (генератор filter)
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_iterator_can_be_consumed_once(
    sample_transactions: list[dict],
) -> None:
    """Тест что итератор можно потребить только один раз"""
    result = filter_by_currency(sample_transactions, "USD")

    # Первое потребление
    first_consumption = list(result)
    assert len(first_consumption) == 3

    # Второе потребление должно дать пустой список
    second_consumption = list(result)
    assert len(second_consumption) == 0


@pytest.mark.parametrize("currency", ["USD", "RUB"])
def test_case_sensitive_currency(
    sample_transactions: list[dict], currency: str
) -> None:
    """Тест чувствительности к регистру валюты"""
    # Фильтр должен быть чувствителен к регистру
    result_upper = list(filter_by_currency(sample_transactions, currency))
    result_lower = list(
        filter_by_currency(sample_transactions, currency.lower())
    )

    # Разный регистр должен давать разные результаты
    if currency.isupper():
        assert len(result_upper) > 0
        assert len(result_lower) == 0


def test_malformed_transactions_skip_or_error(
    malformed_transactions: list[dict],
) -> None:
    """
    Тест обработки транзакций с некорректной структурой.

    Примечание: Текущая реализация вызовет KeyError при отсутствии ключей.
    Это ожидаемое поведение для строгой валидации.
    """

    with pytest.raises(KeyError):
        list(filter_by_currency(malformed_transactions, "USD"))


def test_preserves_transaction_data(sample_transactions: list[dict]) -> None:
    """Тест что данные транзакций сохраняются без изменений"""
    result = list(filter_by_currency(sample_transactions, "USD"))

    for transaction in result:
        # Проверяем что все ключи сохранены
        assert "id" in transaction
        assert "state" in transaction
        assert "date" in transaction
        assert "operationAmount" in transaction
        assert "description" in transaction


def test_filter_by_currency_with_empty_string(
    sample_transactions: list[dict],
) -> None:
    """Тест фильтрации с пустой строкой"""
    result = list(filter_by_currency(sample_transactions, ""))

    assert len(result) == 0


def test_filter_rub_transactions(sample_transactions: list[dict]) -> None:
    """Тест фильтрации транзакций в RUB"""
    result = list(filter_by_currency(sample_transactions, "RUB"))

    assert len(result) == 2
    assert all(
        t["operationAmount"]["currency"]["code"] == "RUB" for t in result
    )
    assert [t["id"] for t in result] == [873106923, 594226727]


def test_filter_nonexistent_currency(sample_transactions: list[dict]) -> None:
    """Тест фильтрации по несуществующей валюте"""
    result = list(filter_by_currency(sample_transactions, "GBP"))

    assert len(result) == 0
    assert result == []


def test_empty_transactions_list(empty_list: list) -> None:
    """Тест обработки пустого списка транзакций"""
    result = list(filter_by_currency(empty_list, "USD"))

    assert len(result) == 0
    assert result == []


def test_no_matching_currency(all_same_currency: list[dict]) -> None:
    """Тест когда нет транзакций в заданной валюте"""
    result = list(filter_by_currency(all_same_currency, "RUB"))

    assert len(result) == 0
    assert isinstance(result, list)


def test_all_same_currency(all_same_currency: list[dict]) -> None:
    """Тест когда все транзакции в одной валюте"""
    result = list(filter_by_currency(all_same_currency, "USD"))

    assert len(result) == 5
    assert len(result) == len(all_same_currency)


def test_single_transaction_match(single_usd_transaction: list[dict]) -> None:
    """Тест одной транзакции с совпадением"""
    result = list(filter_by_currency(single_usd_transaction, "USD"))

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_single_transaction_no_match(
    single_usd_transaction: list[dict],
) -> None:
    """Тест одной транзакции без совпадения"""
    result = list(filter_by_currency(single_usd_transaction, "RUB"))

    assert len(result) == 0


def test_with_transaction_data(sample_transactions: list[dict]) -> None:
    descriptions = transaction_descriptions(sample_transactions)
    # Получаем первые 5 описаний
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_empty_list(empty_list: list) -> None:
    """Тест пустого списка транзакций"""
    descriptions = transaction_descriptions(empty_list)

    with pytest.raises(StopIteration):
        next(descriptions)


def test_missing_description_key(
    transaction_without_description: list[dict],
) -> None:
    """Тест транзакции без ключа 'description'"""
    descriptions = transaction_descriptions(transaction_without_description)

    # Должно вернуть значение по умолчанию
    assert next(descriptions) == "Описание отсутствует"
    assert next(descriptions) == "Перевод организации"


def test_iteration_transactions_with_for_loop(
    sample_transactions: list[dict], expected_descriptions: list
) -> None:
    """Тест итерации через for loop"""
    descriptions = transaction_descriptions(sample_transactions)
    results = [desc for desc in descriptions]

    assert results == expected_descriptions


def test_description_generator_exhaustion() -> None:
    """Тест исчерпания генератора"""
    transactions = [
        {"description": "Описание 1"},
    ]

    descriptions = transaction_descriptions(transactions)

    next(descriptions)  # Получаем единственное описание

    # Повторный вызов должен вызвать StopIteration
    with pytest.raises(StopIteration):
        next(descriptions)


@pytest.mark.parametrize("count", [1, 5, 10, 100])
def test_parametrized_iteration(count: int) -> None:
    """Параметризованный тест для разного количества транзакций"""
    transactions = [{"description": f"Описание {i}"} for i in range(count)]

    descriptions = transaction_descriptions(transactions)
    results = [next(descriptions) for _ in range(count)]

    assert len(results) == count
    assert results[0] == "Описание 0"
    assert results[-1] == f"Описание {count - 1}"


@pytest.mark.parametrize(
    "start,stop,expected_count",
    [
        (1, 5, 5),
        (1, 1, 1),
        (10, 20, 11),
        (100, 100, 1),
        (1, 100, 100),
    ],
)
def test_generator_count(start: int, stop: int, expected_count: int) -> None:
    """Тест количества сгенерированных номеров"""
    cards = list(card_number_generator(start, stop))
    assert len(cards) == expected_count


@pytest.mark.parametrize(
    "start,stop,expected_first,expected_last",
    [
        (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (100, 103, "0000 0000 0000 0100", "0000 0000 0000 0103"),
        (1000, 1002, "0000 0000 0000 1000", "0000 0000 0000 1002"),
    ],
)
def test_generator_range_boundaries(
    start: int, stop: int, expected_first: str, expected_last: str
) -> None:
    """Тест граничных значений диапазона"""
    cards = list(card_number_generator(start, stop))

    assert cards[0] == expected_first, f"Первый номер неверный"
    assert cards[-1] == expected_last, f"Последний номер неверный"


def test_format_correctness(valid_card_ranges: list[tuple]) -> None:
    """Тест правильности форматирования номеров"""
    for start, stop in valid_card_ranges:
        cards = list(card_number_generator(start, stop))

        for card in cards:
            # Проверяем длину (16 цифр + 3 пробела = 19 символов)
            assert len(card) == 19, f"Неверная длина: {card}"

            # Проверяем наличие пробелов на правильных позициях
            assert card[4] == " ", f"Нет пробела после 4-й цифры: {card}"
            assert card[9] == " ", f"Нет пробела после 8-й цифры: {card}"
            assert card[14] == " ", f"Нет пробела после 12-й цифры: {card}"

            # Проверяем что все остальные символы — цифры
            digits_only = card.replace(" ", "")
            assert digits_only.isdigit(), f"Нецифровые символы: {card}"
            assert len(digits_only) == 16, f"Не 16 цифр: {card}"


@pytest.mark.parametrize(
    "start,stop",
    [
        (0, 5),
        (-1, 5),
        (-100, 100),
    ],
)
def test_invalid_start_value(start: int, stop: int) -> None:
    """Тест невалидного начального значения"""
    with pytest.raises(ValueError) as exc_info:
        list(card_number_generator(start, stop))

    assert "Начальное значение" in str(exc_info.value)


@pytest.mark.parametrize(
    "start,stop",
    [
        (1, 10000000000000000),
        (1, 99999999999999999),
        (5, 10000000000000001),
    ],
)
def test_invalid_stop_value(start: int, stop: int) -> None:
    """Тест невалидного конечного значения"""
    with pytest.raises(ValueError) as exc_info:
        list(card_number_generator(start, stop))

    assert "Конечное значение" in str(exc_info.value)


@pytest.mark.parametrize(
    "start,stop",
    [
        (100, 50),
        (1000, 100),
        (999, 1),
    ],
)
def test_start_greater_than_stop(start: int, stop: int) -> None:
    """Тест когда start > stop"""
    with pytest.raises(ValueError) as exc_info:
        list(card_number_generator(start, stop))

    assert "не может быть больше" in str(exc_info.value)


def test_edge_case_minimum() -> None:
    """Тест минимально возможного номера"""
    cards = list(card_number_generator(1, 1))

    assert len(cards) == 1
    assert cards[0] == "0000 0000 0000 0001"


def test_edge_case_maximum() -> None:
    """Тест максимально возможного номера"""
    cards = list(card_number_generator(9999999999999999, 9999999999999999))

    assert len(cards) == 1
    assert cards[0] == "9999 9999 9999 9999"


def test_iteration_with_for_loop(valid_card_ranges: list[tuple]) -> None:
    """Тест итерации через for loop"""
    for start, stop in valid_card_ranges:
        count = 0
        for card in card_number_generator(start, stop):
            count += 1
            assert isinstance(card, str)
            assert len(card) == 19

        assert count == (stop - start + 1)


def test_card_generator_exhaustion() -> None:
    """Тест исчерпания генератора"""
    gen = card_number_generator(1, 3)

    # Получаем все значения
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"

    # Следующий вызов должен вызвать StopIteration
    with pytest.raises(StopIteration):
        next(gen)


def test_zero_padding() -> None:
    """Тест добавления ведущих нулей"""
    test_cases = [
        (1, "0000 0000 0000 0001"),
        (10, "0000 0000 0000 0010"),
        (100, "0000 0000 0000 0100"),
        (1000, "0000 0000 0000 1000"),
        (10000, "0000 0000 0001 0000"),
        (100000, "0000 0000 0010 0000"),
        (1000000, "0000 0000 0100 0000"),
        (10000000, "0000 0000 1000 0000"),
        (100000000, "0000 0001 0000 0000"),
        (1000000000, "0000 0010 0000 0000"),
        (10000000000, "0000 0100 0000 0000"),
        (100000000000, "0000 1000 0000 0000"),
        (1000000000000, "0001 0000 0000 0000"),
        (10000000000000, "0010 0000 0000 0000"),
        (100000000000000, "0100 0000 0000 0000"),
        (1000000000000000, "1000 0000 0000 0000"),
    ]

    for number, expected in test_cases:
        cards = list(card_number_generator(number, number))
        assert cards[0] == expected, f"Failed for {number}"
