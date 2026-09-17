import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


def rename_server_dialog(
        server_detail_page_controller: ServerDetailPageController,
):
    new_name_field = ft.TextField(
        label=ft.Text("Новое название сервера"),
        value=server_detail_page_controller.server_detail_page_state.server.name,
    )

    async def rename_server(e):
        new_name = new_name_field.value.strip()
        await server_detail_page_controller.rename_server(new_name)

    is_server_detail_page_loading = server_detail_page_controller.server_detail_page_state.server_loading_status.value == LoadState.LOADING.value

    return ft.AlertDialog(
        title=ft.Text("Изменение названия сервера"),
        content=new_name_field,
        actions=[
            ft.TextButton(
                "Отмена",
                on_click=server_detail_page_controller.pop_dialog,
                disabled=is_server_detail_page_loading,
            ),
            ft.FilledButton(
                "Сохранить",
                on_click=rename_server,
                disabled=is_server_detail_page_loading,
            ),
        ],
    )
