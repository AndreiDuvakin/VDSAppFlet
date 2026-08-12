import asyncio
import logging

import flet as ft

from ui.pages.billing_page.common import get_years_list_for_consumption_period
from core.contexts import AppContext, BillingPageContext, ApiClientContext
from ui.components.empty_content import empty_content
from ui.components.progress_ring import progress_ring
from ui.components.show_message_banner import show_message_banner
from ui.pages.billing_page.tabs.components.billing_consumption_view import billing_consumption_view

logger = logging.getLogger(__name__)


@ft.component
def consumption_operations_tab():
    app_state = ft.use_context(AppContext)
    billing_page_state = ft.use_context(BillingPageContext)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    years_list = ft.use_memo(
        lambda: get_years_list_for_consumption_period(app_state.account.info.actdate),
        [app_state.account.info.actdate]
    )
    selected_index = billing_page_state.current_year_consumption_index

    async def get_billing_consumption(index):
        try:
            logger.info("Getting billing consumption")
            billing_page_state.set_is_billing_consumption_loading(True)

            selected_year = years_list[index]

            await asyncio.sleep(2)

            billing_consumption = await api_client.billing_service.get_billing_new_consumption(selected_year)
            billing_page_state.set_billing_consumption(billing_consumption)

            logger.info("Billing consumption loaded")
        except Exception as e:
            logger.error(f'Error getting billing consumption: {e}')
            show_message_banner(
                "Ошибка получения списка операций списания.",
                page,
            )

        finally:
            logger.info("Getting billing consumption finished")
            billing_page_state.set_is_billing_consumption_loading(False)

    def handle_select_year(e):
        index = e.control.selected_index
        on_select_year(index)

    def on_select_year(index):
        if index is None:
            return

        billing_page_state.set_current_year_index(index)

        asyncio.create_task(get_billing_consumption(index))

    segment_button = ft.Row(
        [
            ft.CupertinoSlidingSegmentedButton(
                selected_index=selected_index,
                on_change=handle_select_year,
                controls=[
                    ft.Text(str(year))
                    for year in years_list
                ],
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    if billing_page_state.is_billing_consumption_loading:
        return ft.Column(
            [
                segment_button,
                progress_ring(),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    if not billing_page_state.billing_consumption and not billing_page_state.is_billing_consumption_loading:
        on_select_year(selected_index)

    if not years_list or not billing_page_state.billing_consumption:
        return empty_content(
            ft.Icons.RECEIPT_LONG_OUTLINED,
            "Нет операций для отображения",
            "Возможно они не были загружены или произошла ошибка",
        )

    return ft.Column(
        [
            segment_button,
            ft.Container(
                content=billing_consumption_view(
                    billing_page_state.billing_consumption,
                ),
                expand=True,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
