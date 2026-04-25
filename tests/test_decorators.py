import os
import tempfile

import pytest

from src.decorators import log


def test_log_to_console_on_success(sample_functions, capsys, cleanup_logging):
    """Тест логирования в консоль при успешном выполнении"""
    result = sample_functions["add"](2, 3)

    assert result == 5

    captured = capsys.readouterr()
    assert "add_numbers ok" in captured.err


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
        (1.5, 2.5, 4.0),
    ],
)
def test_log_with_different_inputs_console(
    x, y, expected, sample_functions, capsys, cleanup_logging
):
    """Тест с разными входными данными и проверкой консоли"""

    result = sample_functions["add"](x, y)

    assert result == expected

    captured = capsys.readouterr()
    assert "add_numbers ok" in captured.err


def test_log_to_file_on_success(temp_log_file, cleanup_logging):
    """Тест логирования в файл при успешном выполнении"""

    @log(filename=temp_log_file)
    def test_func(x, y):
        return x + y

    result = test_func(1, 2)

    assert result == 3

    # Читаем файл и проверяем лог
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "test_func ok" in log_content


def test_log_function_name(temp_log_file, cleanup_logging):
    """Тест что имя функции правильно записывается в лог"""

    @log(filename=temp_log_file)
    def my_custom_function_name():
        return 1

    my_custom_function_name()

    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "my_custom_function_name ok" in log_content


def test_log_multiple_calls(temp_log_file, cleanup_logging):
    """Тест множественных вызовов функции"""

    @log(filename=temp_log_file)
    def increment(x):
        return x + 1

    increment(1)
    increment(2)
    increment(3)

    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    # Должно быть 3 записи
    assert log_content.count("increment ok") == 3


def test_log_function_with_kwargs(temp_log_file, cleanup_logging):
    """Тест функции с keyword аргументами"""

    @log(filename=temp_log_file)
    def func_with_kwargs(a, b=10, c=20):
        return a + b + c

    result = func_with_kwargs(1, b=2, c=3)

    assert result == 6

    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "func_with_kwargs ok" in log_content


def test_log_function_no_args(temp_log_file, cleanup_logging):
    """Тест функции без аргументов"""

    @log(filename=temp_log_file)
    def no_args():
        return 42

    result = no_args()

    assert result == 42

    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "no_args ok" in log_content


def test_log_function_returns_none(temp_log_file, cleanup_logging):
    """Тест функции возвращающей None"""

    @log(filename=temp_log_file)
    def returns_none():
        pass

    result = returns_none()

    assert result is None

    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "returns_none ok" in log_content


def test_log_error_with_kwargs_console(
    sample_functions, capsys, cleanup_logging
):
    """Тест логирования ошибки с kwargs"""

    with pytest.raises(RuntimeError):
        sample_functions["kwargs"](1, b=20)

    captured = capsys.readouterr()

    assert "error_with_kwargs error: RuntimeError" in captured.err
    assert "Inputs: (1,), {'b': 20}" in captured.err


def test_log_value_error_console(sample_functions, capsys, cleanup_logging):
    """Тест логирования ValueError в консоль"""

    # Ожидает что исключение будет выброшено
    with pytest.raises(ValueError):
        sample_functions["value_error"](42)

    captured = capsys.readouterr()

    # Проверяем что ошибка залогирована в stderr
    assert "raise_value_error error: ValueError" in captured.err
    assert "Inputs: (42,), {}" in captured.err


def test_log_type_error_console(sample_functions, capsys, cleanup_logging):
    """Тест логирования TypeError в консоль"""

    with pytest.raises(TypeError):
        sample_functions["type_error"]("a", "b")

    captured = capsys.readouterr()

    assert "raise_type_error error: TypeError" in captured.err
    assert "Inputs: ('a', 'b'), {}" in captured.err


def test_log_key_error_console(sample_functions, capsys, cleanup_logging):
    """Тест логирования KeyError"""

    with pytest.raises(KeyError):
        sample_functions["key_error"]()

    captured = capsys.readouterr()

    assert "raise_key_error error: KeyError" in captured.err


def test_capsys_readouterr_consumes_output(capsys, cleanup_logging):
    """
    Тест что readouterr() потребляет вывод.
    После первого вызова вывод очищается.
    """

    @log(filename=None)
    def test_func():
        return 1

    test_func()

    # Первый перехват
    captured1 = capsys.readouterr()
    assert "test_func ok" in captured1.err

    # Второй перехват — вывод уже потреблён
    captured2 = capsys.readouterr()
    assert "test_func ok" not in captured2.err


def test_capsys_with_print_and_log(capsys, cleanup_logging):
    """Тест комбинации print() и логирования"""

    @log(filename=None)
    def func_with_print(x):
        print(f"Processing {x}")
        return x * 2

    result = func_with_print(5)

    assert result == 10

    captured = capsys.readouterr()

    # print() идёт в stdout
    assert "Processing 5" in captured.out

    # Логирование идёт в stderr
    assert "func_with_print ok" in captured.err


def test_capsys_reset_between_tests(capsys, cleanup_logging):
    """
    Тест что capsys сбрасывается между тестами.
    Это гарантирует изоляцию тестов.
    """

    @log(filename=None)
    def test_a():
        return 1

    test_a()

    captured = capsys.readouterr()
    assert "test_a ok" in captured.err

    # В этом тесте не должно быть вывода от test_a
    # потому что capsys сбрасывается между тестами автоматически


def test_capsys_with_nested_functions(capsys, cleanup_logging):
    """Тест вложенных функций с логированием"""

    @log(filename=None)
    def outer():
        inner()
        return "outer"

    @log(filename=None)
    def inner():
        return "inner"

    result = outer()

    assert result == "outer"

    captured = capsys.readouterr()

    # Должны быть логи обеих функций
    assert "outer ok" in captured.err
    assert "inner ok" in captured.err


def test_log_to_file_no_console_output(temp_log_file, capsys, cleanup_logging):
    """
    Тест что при логировании в файл вывод в консоль отсутствует.
    """

    @log(filename=temp_log_file)
    def file_func():
        return 1

    file_func()

    captured = capsys.readouterr()

    # В консоли не должно быть вывода
    assert "file_func ok" not in captured.out
    assert "file_func ok" not in captured.err

    # Но в файле должно быть
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "file_func ok" in log_content


def test_log_to_console_no_file_created(capsys, cleanup_logging):
    """
    Тест что при логировании в консоль файл не создаётся.
    """

    temp_path = os.path.join(tempfile.gettempdir(), "should_not_exist.log")

    # Гарантируем что файла нет
    if os.path.exists(temp_path):
        os.remove(temp_path)

    @log(filename=None)
    def console_func():
        return 1

    console_func()

    captured = capsys.readouterr()

    # В консоли должен быть вывод
    assert "console_func ok" in captured.err

    # Файл не должен существовать
    assert not os.path.exists(temp_path)
