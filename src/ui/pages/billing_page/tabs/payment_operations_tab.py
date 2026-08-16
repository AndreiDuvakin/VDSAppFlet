import asyncio
import logging

import flet as ft

from ui.pages.billing_page.common import group_operations_by_year_month
from core.contexts import BillingPageContext, ApiClientContext
from ui.components.empty_content import empty_content
from ui.components.progress_ring import progress_ring
from ui.components.show_message_banner import show_message_banner
from ui.pages.billing_page.tabs.components.billing_operations_view import (
    billing_operations_view,
)

logger = logging.getLogger(__name__)


@ft.component
def payment_operations_tab():
    billing_page_state = ft.use_context(BillingPageContext)
    api_client = ft.use_context(ApiClientContext)

    page = ft.context.page

    async def get_billing_payments():
        try:
            logger.info("Getting billing payments")
            billing_page_state.set_is_billing_payment_loading(True)

            billing_payments = await api_client.billing_service.get_billing_payments()

            parsed_billing_payments = await group_operations_by_year_month(
                billing_payments.items,
            )

            logger.info("Billing payments loaded")
            billing_page_state.set_billing_payments(
                parsed_billing_payments,
            )

        except Exception:
            logger.exception("Error getting billing payments")

            show_message_banner(
                "Ошибка получения списка операций пополнений.",
                page,
            )

        finally:
            billing_page_state.set_is_billing_payment_loading(False)

    if (
        billing_page_state.billing_payments is None
        and not billing_page_state.is_billing_payment_loading
    ):
        asyncio.create_task(get_billing_payments())

    if billing_page_state.is_billing_payment_loading:
        return progress_ring()

    if billing_page_state.billing_payments is None:
        logger.info("Billing payments not present")

        return empty_content(
            ft.Icons.PAYMENT,
            "Нет данных о пополнениях",
            "Возможно во время загрузки произошло ошибка",
        )

    return ft.Column(
        [
            billing_operations_view(billing_page_state.billing_payments),
        ],
        expand=True,
    )
