import logging

from src.api.price_client import PriceClient
from src.models.price import GetPrice

logger = logging.getLogger(__name__)


class PriceService:
    def __init__(self, price_client: PriceClient) -> None:
        logger.info("Initializing Price Service")

        self._client = price_client

    async def get_price(self) -> GetPrice:
        logger.info("Getting Servers")

        return await self._client.get_price()
