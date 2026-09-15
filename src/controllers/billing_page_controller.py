import asyncio
import logging
from typing import Callable

from src.models.billing import BillingOperation
from src.services.billing_service import BillingService
from src.state.billing_page_state import BillingPageState
from src.state.load_state import LoadState
from src.ui.pages.billing_page.common import group_operations_by_year_month_sync

logger = logging.getLogger(__name__)


class BillingPageController:
    def __init__(
        self,
        billing_service: BillingService,
        billing_page_state: BillingPageState,
        show_message_banner: Callable[[str, bool], None],
    ):
        self._billing_service = billing_service
        self._billing_page_state = billing_page_state
        self.show_message_banner = show_message_banner

    async def get_billing_balance(self):
        try:
            self._billing_page_state.set_balance_loading_status(LoadState.LOADING)

            logger.info("Getting billing balance")
            balance = await self._billing_service.get_billing_balance()
            self._billing_page_state.set_balance(balance.balance)
            logger.info("Balance is loaded")

        except Exception as e:
            self._billing_page_state.set_balance_loading_status(LoadState.ERROR)
            logger.exception(f"Error getting billing balance: {e}")
            self.show_message_banner(
                "Ошибка получения баланса.",
                True,
            )

        else:
            self._billing_page_state.set_balance_loading_status(LoadState.SUCCESS)

    async def repeat_get_billing_balance(self):
        logger.info("Trying to get billing balance again")
        await self._billing_service.get_billing_balance()

    async def get_billing_payments(self):
        try:
            logger.info("Getting billing payments")
            self._billing_page_state.set_billing_payment_loading_status(
                LoadState.LOADING
            )

            billing_payments = await self._billing_service.get_billing_payments()

            parsed_billing_payments = await self._group_operations_by_year_month(
                billing_payments.items,
            )

            logger.info("Billing payments loaded")
            self._billing_page_state.set_billing_payments(
                parsed_billing_payments,
            )

        except Exception as e:
            self._billing_page_state.set_billing_payment_loading_status(LoadState.ERROR)
            logger.exception(f"Error getting billing payments: {e}")

            self.show_message_banner(
                "Ошибка получения списка операций пополнений.",
                True,
            )

        else:
            self._billing_page_state.set_billing_payment_loading_status(
                LoadState.SUCCESS
            )

    async def repeat_get_billing_payments(self):
        logger.info("Trying to get billing payments again")
        await self._billing_service.get_billing_payments()

    async def get_billing_consumption(self, selected_year):
        try:
            logger.info("Getting billing consumption")
            self._billing_page_state.set_billing_consumption_loading_status(
                LoadState.LOADING
            )

            await asyncio.sleep(2)

            billing_consumption = (
                await self._billing_service.get_billing_new_consumption(selected_year)
            )
            self._billing_page_state.set_billing_consumption(billing_consumption)

            logger.info("Billing consumption loaded")
        except Exception as e:
            self._billing_page_state.set_billing_consumption_loading_status(
                LoadState.ERROR
            )
            logger.error(f"Error getting billing consumption: {e}")
            self.show_message_banner(
                "Ошибка получения списка операций списания.",
                True,
            )

        else:
            logger.info("Billing consumption loaded")
            self._billing_page_state.set_billing_consumption_loading_status(
                LoadState.SUCCESS
            )

    async def repeat_get_billing_consumption(self):
        logger.info("Trying to get billing consumption again")
        await self.get_billing_consumption()

    @staticmethod
    async def _group_operations_by_year_month(
        billing_operations: list[BillingOperation],
    ) -> dict[int, dict[int, list[BillingOperation]]]:
        return await asyncio.to_thread(
            group_operations_by_year_month_sync,
            billing_operations,
        )
