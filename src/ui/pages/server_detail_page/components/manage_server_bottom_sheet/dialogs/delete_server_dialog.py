import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController

logger = logging.getLogger(__name__)


def delete_server_dialog(
    server_detail_page_controller: ServerDetailPageController,
):
    server = server_detail_page_controller.server_detail_page_state.server

    async def confirm_delete(e):
        server_detail_page_controller.pop_dialog()
        await server_detail_page_controller.delete_server()

    return ft.AlertDialog(
        title=ft.Text("Удаление сервера"),
        content=ft.Text(
            f"Вы уверены, что хотите удалить сервер '{server.name}'?\n"
            "Это действие нельзя отменить."
        ),
        actions=[
            ft.TextButton("Отмена", on_click=server_detail_page_controller.pop_dialog),
            ft.FilledButton(
                "Подтвердить", on_click=confirm_delete, color=ft.Colors.RED_400
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
