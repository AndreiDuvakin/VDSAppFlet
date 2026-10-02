import datetime
import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController

logger = logging.getLogger(__name__)


def create_backup_server_dialog(
    server_detail_page_controller: ServerDetailPageController,
):
    server = server_detail_page_controller.server_detail_page_state.server

    current_date = datetime.date.today().strftime("%Y%m%d")
    backup_default_name = f"{server.name}_backup_{current_date}"

    backup_name_field = ft.TextField(
        label="Название бэкапа",
        value=backup_default_name,
    )

    async def confirm_create_backup(e):
        backup_name = backup_name_field.value.strip()

        if not backup_name:
            server_detail_page_controller.show_simple_dialog(
                "Пустое название",
                "Введите название бэкапа",
            )
            return

        server_detail_page_controller.pop_dialog()

        await server_detail_page_controller.create_server_backup(backup_name)

    return ft.AlertDialog(
        title=ft.Text("Создание бэкапа"),
        content=backup_name_field,
        actions=[
            ft.TextButton("Отмена", on_click=server_detail_page_controller.pop_dialog),
            ft.FilledButton(
                "Подтвердить",
                on_click=confirm_create_backup,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
