from dataclass_rest import get

from src.api.abstract_client import AbstractClient
from src.models.billing import GetBillingBalance, GetBillingOperations


class BillingClient(AbstractClient):
    @get("billing/balance")
    async def get_billing_balance(self) -> GetBillingBalance:
        pass

    @get("billing/payments")
    async def get_billing_payments(self) -> GetBillingOperations:
        pass

    @get("billing/new_consumption?year={year}")
    async def get_billing_new_consumption(self, year: int) -> dict:
        pass
