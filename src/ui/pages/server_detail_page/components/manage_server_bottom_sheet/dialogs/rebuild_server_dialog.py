import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController

logger = logging.getLogger(__name__)


def rebuild_server_dialog(
    server_detail_page_controller: ServerDetailPageController,
):
    server = server_detail_page_controller.server_detail_page_state.server

    async def confirm_rebuild(e):
        server_detail_page_controller.pop_dialog()
        await server_detail_page_controller.rebuild_server()

    return ft.AlertDialog(
        title=ft.Text("Переустановка сервера"),
        content=ft.Text(
            f"Вы уверены, что хотите переустановить "
            f"операционную систему сервера '{server.name}'?\n"
            "Это действие нельзя отменить."
        ),
        actions=[
            ft.TextButton("Отмена", on_click=server_detail_page_controller.pop_dialog),
            ft.FilledButton(
                "Подтвердить", on_click=confirm_rebuild, color=ft.Colors.RED_400
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
