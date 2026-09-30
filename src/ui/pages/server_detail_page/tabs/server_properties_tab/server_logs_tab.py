import asyncio
import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.core.contexts import ServerDetailPageContext
from src.state.load_state import LoadState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.components.progress_ring import progress_ring

logger = logging.getLogger(__name__)


@ft.component
def server_logs_tab(
    server_detail_page_controller: ServerDetailPageController,
):
    server_detail_page_state = ft.use_context(ServerDetailPageContext)

    if (
        server_detail_page_state.server_logs_list is None
        and server_detail_page_state.logs_loading_status.value == LoadState.IDLE.value
    ):
        logger.info("Servers logs not loaded, starting loading")
        asyncio.create_task(server_detail_page_controller.get_server_logs())

    if server_detail_page_state.logs_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить SSH ключи",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            server_detail_page_controller.repeat_load_server_logs,
        )

    if server_detail_page_state.logs_loading_status.value == LoadState.LOADING.value:
        return progress_ring()

    if not server_detail_page_state.server_logs_list:
        return empty_content(
            ft.Icons.CLOUD_OFF,
            "Нет логов для отображения",
            "Возможно они не были загружены",
        )

    return ft.Column(
        [
            ft.DataTable(
                columns=[
                    ft.DataColumn(
                        label=ft.Text("Что произошло", weight=ft.FontWeight.BOLD)
                    ),
                    ft.DataColumn(label=ft.Text("Когда", weight=ft.FontWeight.BOLD)),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(log.status_text)),
                            ft.DataCell(ft.Text(log.date)),
                        ]
                    )
                    for log in server_detail_page_state.server_logs_list
                ],
                expand=True,
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
