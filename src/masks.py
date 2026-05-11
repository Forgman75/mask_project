import logging
from pathlib import Path

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Настроен file_handler для логера модуля masks
log_file_path = log_dir / "masks.log"
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настроен file_formatter для логера модуля masks
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Эта функция принимает номер карты ввиде целого числа,
    а возвращает строку из первых шести цифр, шести звездочек
    и последних четырех цифр.
    """

    logger.debug(f"Попытка маскировки номера: {card_number}")
    try:
        if not isinstance(card_number, int):
            raise TypeError(f"Expected int, got {type(card_number).__name__}")

        card_number_string = str(card_number)
        stars_string = (
            f"{card_number_string[0:6]}******{card_number_string[-4:]}"
        )
        split_string = " ".join(
            stars_string[i * 4 : (i + 1) * 4] for i in range(4)
        )

        logger.info(f"Номер карты успешно замаскирован: {split_string}")
        return split_string

    except TypeError as e:
        logger.error(f"Номер карты должен быть целым числом: {e}")
        raise

    except Exception as e:
        logger.error(f"Непредвиденная ошибка при маскировке: {e}")
        raise


def get_mask_account(account_number: int) -> str:
    """
    Эта функция преобразует номер счета из целого числа
    в строку из двух звездочек в начале и четырех последних цифр
    в конце.
    """

    logger.debug(f"Попытка маскировки счета: {account_number}")
    try:
        if not isinstance(account_number, int):
            raise TypeError(
                f"Expected int, got {type(account_number).__name__}"
            )

        account_number_string = str(abs(account_number))
        result_account = f"**{account_number_string[-4:]}"
        logger.info(f"Номер счета успешно замаскирован: {result_account}")
        return result_account

    except TypeError as e:
        logger.error(f"Номер счета должен быть целым числом: {e}")
        raise

    except Exception as e:
        logger.error(f"Непредвиденная ошибка при маскировке: {e}")
        raise
