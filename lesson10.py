"""
Модуль для работы с валютами и ценами.

Описание модуля и его функциональности.
"""
import json
import time
from dataclasses import dataclass
from datetime import datetime

import requests

ALPHAVANTAGE_API_KEY = "6I2HOYT0DOXGAH5T"
MIDDLE_CURRENCY = "CHF"


def convert(value: float, currency_from: str, currency_to: str) -> float:
    start_time = time.time()
    response: requests.Response = requests.get(
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey={ALPHAVANTAGE_API_KEY}",
        timeout=10,
    )
    result: dict = response.json()
    coefficient: float = float(
        result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )
    end_time = time.time()
    execution_time = end_time - start_time
    with open("logs.json", mode="a", encoding="utf-8") as logs_file:
        logs_entry = {
            "timestamp": datetime.now().isoformat(),
            "value": value,
            "currency_from": currency_from,
            "currency_to": currency_to,
            "coefficient": coefficient,
            "converted_value": value * coefficient,
            "rate": execution_time,
        }
        json.dump(logs_entry, logs_file)
        logs_file.write("\n")
    return value * coefficient


@dataclass
class Price:
    value: float
    currency: str

    def __add__(self, other: "Price") -> "Price":
        print("add")
        if self.currency == other.currency:
            return Price(value=self.value + other.value, currency=self.currency)

        left_in_middle: float = convert(
            value=self.value,
            currency_from=self.currency,
            currency_to=MIDDLE_CURRENCY,
        )
        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle + right_in_middle
        total_in_left_currency: float = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=self.currency,
        )
        return Price(value=total_in_left_currency, currency=self.currency)


flight = Price(value=1, currency="USD")
hotel = Price(value=1, currency="EUR")
total = flight + hotel
print(total)
