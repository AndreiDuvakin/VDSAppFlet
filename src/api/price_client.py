from dataclass_rest import get

from src.api.abstract_client import AbstractClient
from src.models.price import GetPrice


class PriceClient(AbstractClient):
    @get("billing/prices")
    async def get_price(self) -> GetPrice:
        pass
