from src.widget import get_date, mask_account_card


def main():
    DATE_STR_ISO = "2024-03-11T02:26:18.671407"

    list_of_payment = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]
    for i in range(len(list_of_payment)):
        print(mask_account_card(list_of_payment[i]))

    print(get_date(DATE_STR_ISO))


if __name__ == "__main__":
    main()
