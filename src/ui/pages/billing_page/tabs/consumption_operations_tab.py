import asyncio
import logging

import flet as ft

from core.common import group_operations_by_year_month
from core.contexts import BillingPageContext, ApiClientContext
from ui.components.progress_ring import progress_ring
from ui.components.show_message_banner import show_message_banner
from ui.pages.billing_page.tabs.components.billing_operations_view import billing_operations_view

logger = logging.getLogger(__name__)


@ft.component
def consumption_operations_tab():
    billing_page_state = ft.use_context(BillingPageContext)
    api_client = ft.use_context(ApiClientContext)

    page = ft.context.page

    async def get_billing_payments():
        try:
            logger.info('Getting billing payments')
            billing_page_state.set_is_billing_payment_loading(True)

            billing_payments = (
                await api_client.billing_service.get_billing_payments()
            )

            parsed_billing_payments = (
                await group_operations_by_year_month(
                    billing_payments.items,
                )
            )

            logger.info('Billing payments loaded')
            billing_page_state.set_billing_payments(
                parsed_billing_payments,
            )

        except Exception:
            logger.exception('Error getting billing payments')

            show_message_banner(
                'Ошибка получения списка списаний.',
                page,
            )

        finally:
            billing_page_state.set_is_billing_payment_loading(False)



    if billing_page_state.billing_payments is None and not billing_page_state.is_billing_payment_loading:
        asyncio.create_task(get_billing_payments())

    if billing_page_state.is_billing_payment_loading:
        return progress_ring()

    if billing_page_state.billing_payments is None:
        logger.info(f"Billing payments not present")

        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.PAYMENT, size=64, color=ft.Colors.GREY_400),
                            ft.Text("Нет данных о списаниях", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Возможно во время загрузки произошло ошибка",
                                size=14,
                                color=ft.Colors.GREY_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            expand=True,
        )

    return ft.Column(
        [
            billing_operations_view(
                billing_page_state.billing_payments
            ),
        ],
        expand=True,
    )
