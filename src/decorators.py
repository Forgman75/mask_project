import functools
import logging
from pathlib import Path
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.

    Логирует успешное выполнения функции или ошибки.

    Args:
        filename: Путь к файлу для записи логов.
                  Если None, логи выводятся в консоль.

    Returns:
        Callable: Декоратор для функции.

    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Настраиваем логгер
            logger = _get_logger(filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                logger.info(f"{func.__name__} ok")

                return result

            except Exception as e:
                # Логируем ошибку
                error_type = type(e).__name__
                logger.error(
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}"
                )

                # Перевыбрасываем исключение
                raise

        return wrapper

    return decorator


def _get_logger(filename: str | None) -> logging.Logger:
    """
    Создаёт или получает настроенный логгер.

    Args:
        filename: Путь к файлу для записи логов, или None для консоли.

    Returns:
        logging.Logger: Настроенный логгер.
    """
    logger_name = "function_logger"
    logger = logging.getLogger(logger_name)

    # Очищаем существующие обработчики чтобы не дублировать логи
    logger.handlers.clear()
    logger.setLevel(logging.INFO)

    # Создаём форматтер (только сообщение, без времени и уровня)
    formatter = logging.Formatter("%(message)s")

    if filename:
        # Создаём директорию если не существует
        log_path = Path(filename)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # File handler
        file_handler = logging.FileHandler(
            filename, mode="a", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Отключаем propagate чтобы не дублировать в root logger
    logger.propagate = False

    return logger
