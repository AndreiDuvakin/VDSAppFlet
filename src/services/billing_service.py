import logging

from src.api.billing_client import BillingClient
from src.models.billing import BillingUsage, GetBillingBalance, GetBillingOperations
from src.ui.pages.billing_page.common import group_usage_by_period, parse_billing_usage

logger = logging.getLogger(__name__)


class BillingService:
    def __init__(self, billing_client: BillingClient):
        logger.info("Initializing BillingService")

        self._client = billing_client

    async def get_billing_balance(self) -> GetBillingBalance:
        logger.info("Getting billing balance")

        return await self._client.get_billing_balance()

    async def get_billing_payments(self) -> GetBillingOperations:
        logger.info("Getting billing payments")

        return await self._client.get_billing_payments()

    async def get_billing_new_consumption(
        self, year
    ) -> dict[int, dict[int, list[BillingUsage]]]:
        logger.info("Getting billing new consumption")

        result = await self._client.get_billing_new_consumption(year)

        return group_usage_by_period(parse_billing_usage(result))
