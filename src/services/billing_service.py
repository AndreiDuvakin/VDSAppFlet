import logging
from typing import List

from api.billing_client import BillingClient
from core.common import parse_billing_usage, group_usage_by_period
from models.billing import GetBillingBalance, GetBillingOperations, BillingUsage

logger = logging.getLogger(__name__)


class BillingService:
    def __init__(self, billing_client: BillingClient):
        logger.info('Initializing BillingService')

        self._client = billing_client

    async def get_billing_balance(self) -> GetBillingBalance:
        logger.info('Getting billing balance')

        return await self._client.get_billing_balance()

    async def get_billing_payments(self) -> GetBillingOperations:
        logger.info('Getting billing payments')

        return await self._client.get_billing_payments()

    async def get_billing_new_consumption(self, year) -> dict[int, dict[int, list[BillingUsage]]]:
        logger.info('Getting billing new consumption')

        result = await self._client.get_billing_new_consumption(year)

        return group_usage_by_period(
            parse_billing_usage(
                result
            )
        )
