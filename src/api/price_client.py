from dataclass_rest import get

from api.abstract_client import AbstractClient
from models.price import GetPrice


class PriceClient(AbstractClient):
    @get('billing/prices')
    async def get_price(self) -> GetPrice:
        pass
