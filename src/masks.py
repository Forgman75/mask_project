def get_mask_card_number(card_number: int) -> str:
    """
    Эта функция принимает номер карты ввиде целого числа,
    а возвращает строку из первых шести цифр, шести звездочек
    и последних четырех цифр.
    """

    if not isinstance(card_number, int):
        raise TypeError(f"Expected int, got {type(card_number).__name__}")

    card_number_string = str(card_number)
    stars_string = f"{card_number_string[0:6]}******{card_number_string[-4:]}"
    split_string = " ".join(
        stars_string[i * 4 : (i + 1) * 4] for i in range(4)
    )

    return split_string


def get_mask_account(account_number: int) -> str:
    """
    Эта функция преобразует номер счета из целого числа
    в строку из двух звездочек в начале и четырех последних цифр
    в конце.
    """
    account_number_string = str(account_number)
    return f"**{account_number_string[-4:]}"
