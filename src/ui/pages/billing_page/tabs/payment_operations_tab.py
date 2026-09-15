import asyncio
import logging

import flet as ft

from src.controllers.billing_page_controller import BillingPageController
from src.core.contexts import BillingPageContext
from src.state.load_state import LoadState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.components.progress_ring import progress_ring
from src.ui.pages.billing_page.tabs.components.billing_operations_view import (
    billing_operations_view,
)

logger = logging.getLogger(__name__)


@ft.component
def payment_operations_tab(
    billing_page_controller: BillingPageController,
):
    billing_page_state = ft.use_context(BillingPageContext)

    if (
        billing_page_state.billing_payments is None
        and not billing_page_state.billing_payment_loading_status.value
        == LoadState.LOADING.value
    ):
        asyncio.create_task(billing_page_controller.get_billing_payments())

    if (
        billing_page_state.billing_payment_loading_status.value
        == LoadState.LOADING.value
    ):
        return progress_ring()

    if billing_page_state.billing_payment_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить список операций",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            billing_page_controller.repeat_get_billing_payments,
        )

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
