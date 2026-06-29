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

    from_acc = transaction.get("from", "") or ""
    to_acc = transaction.get("to", "") or ""

    # Маскируем только непустые значения
    if from_acc:
        from_acc = mask_account_card(from_acc)
    if to_acc:
        to_acc = mask_account_card(to_acc)

    # Стрелка только если оба поля заполнены
    if from_acc and to_acc:
        account_line = f"{from_acc} -> {to_acc}"
    elif to_acc:
        account_line = to_acc
    elif from_acc:
        account_line = from_acc
    else:
        account_line = ""

    op = transaction.get("operationAmount", {}) or {}
    amount = _format_amount(op.get("amount", "0"))
    currency = (op.get("currency", {}) or {}).get("name", "")

    lines = [f"{date_line} {description}"]
    if account_line:
        lines.append(account_line)
    lines.append(f"Сумма: {amount} {currency}")

    return "\n".join(lines)


