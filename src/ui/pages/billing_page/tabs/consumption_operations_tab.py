import asyncio
import logging

import flet as ft

from src.controllers.billing_page_controller import BillingPageController
from src.core.contexts import AppContext, BillingPageContext
from src.state.load_state import LoadState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.components.progress_ring import progress_ring
from src.ui.pages.billing_page.common import get_years_list_for_consumption_period
from src.ui.pages.billing_page.tabs.components.billing_consumption_view import (
    billing_consumption_view,
)

logger = logging.getLogger(__name__)


@ft.component
def consumption_operations_tab(
    billing_page_controller: BillingPageController,
):
    app_state = ft.use_context(AppContext)
    billing_page_state = ft.use_context(BillingPageContext)
    selected_year_index, set_selected_year_index = ft.use_state(None)

    years_list = ft.use_memo(
        lambda: get_years_list_for_consumption_period(app_state.account.info.actdate),
        [app_state.account.info.actdate],
    )
    selected_index = billing_page_state.current_year_consumption_index

    async def repeat_get_billing_consumption():
        if selected_year_index is None:
            billing_page_controller.show_message_banner(
                "Невозможно повторить загрузку: год не выбран",
                True,
            )
            return

        await get_billing_consumption(selected_year_index)

    def handle_select_year(e):
        index = e.control.selected_index
        set_selected_year_index(index)
        on_select_year(index)

    async def get_billing_consumption(index):
        selected_year = years_list[index]
        await billing_page_controller.get_billing_consumption(selected_year)

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
                controls=[ft.Text(str(year)) for year in years_list],
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    if (
        billing_page_state.billing_consumption_loading_status.value
        == LoadState.LOADING.value
    ):
        return ft.Column(
            [
                segment_button,
                progress_ring(),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    if (
        not billing_page_state.billing_consumption
        and billing_page_state.billing_consumption_loading_status.value
        == LoadState.IDLE.value
    ):
        on_select_year(selected_index)

    if (
        billing_page_state.billing_consumption_loading_status.value
        == LoadState.ERROR.value
    ):
        return error_content(
            "Не удалось загрузить список операций",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            repeat_get_billing_consumption,
        )

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
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
