import os

import requests
from dotenv import load_dotenv

API_BASE_URL = "https://v6.exchangerate-api.com/v6/"
TARGET_CURRENCY = "RUB"


def convert_currency_at_rate(
    amount: float, from_currency: str, to_currency: str = TARGET_CURRENCY
) -> float:
    """
    Получает сумму в рублях по текущему курсу валюты через ExchangeRate-API.

    Args:
        from_currency: Код исходной валюты (USD, EUR)
        to_currency: Код целевой валюты (по умолчанию RUB)

    Returns:
        float: Сумма в рублях после конвертации
    """
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", ".env")
    load_dotenv(file_path)

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError(
            "EXCHANGE_RATE_API_KEY не найден в переменных окружения"
        )

    bearer = "Bearer {token}".format(token=api_key)
    headers = {"Authorization": bearer}

    URL = f"{API_BASE_URL}/pair/{from_currency}/{to_currency}/{amount}"

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("result") == "error":
            raise RuntimeError(
                f"API error: {data.get('error-type', 'Unknown error')}"
            )

        result = data.get("conversion_result", {})
        if result is None:
            raise ValueError(f"Курс для {to_currency} не найден в ответе API")

        return float(result)

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка запроса к API: {e}")
