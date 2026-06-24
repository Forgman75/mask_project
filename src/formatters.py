from datetime import datetime
from src.widget import mask_account_card, get_date


def _format_amount(amount_str: str) -> str:
    try:
        value = float(amount_str)
        if value == int(value):
            return str(int(value))
        return str(value)
    except (ValueError, TypeError):
        return str(amount_str or "0")


def format_transaction(transaction: dict) -> str:
    """
    Форматирует одну транзакцию для вывода в консоль.
    """
    date_line = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    from_acc = mask_account_card(transaction.get("from", "")) or ""
    to_acc = mask_account_card(transaction.get("to", "")) or ""

    if from_acc:
        account_line = f"{from_acc} -> {to_acc}"
    else:
        account_line = to_acc

    op = transaction.get("operationAmount", {}) or {}
    amount = _format_amount(op.get("amount", "0"))
    currency = (op.get("currency", {}) or {}).get("name", "")

    return (f"{date_line} {description}\n{account_line}\n"
            f"Сумма: {amount} {currency}")

