from dataclasses import dataclass
from datetime import datetime


@dataclass
class Price:
    hour: int
    month: int


@dataclass
class DefaultPrice:
    huge: Price
    large: Price
    medium: Price
    monster: Price
    small: Price
    backup: int | None = None


@dataclass
class GetPrice:
    default: DefaultPrice
    period: datetime

    def get_price_by_rplan(self, rplan: str) -> Price | None:
        if rplan == "backup":
            raise ValueError("backup is not a Price")

        price = getattr(self.default, rplan, None)

        if price is None:
            raise ValueError(f"Unknown rplan: {rplan}")

        return price

    def get_month_price_beautiful(self, rplan: str) -> str | None:
        price = self.get_price_by_rplan(rplan)

        if price is None:
            return None

        total_price = round(price.month / 100)

        return f'{total_price} ₽'
