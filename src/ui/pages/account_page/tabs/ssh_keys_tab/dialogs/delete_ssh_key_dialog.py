import logging

import flet as ft

from src.controllers.account_page_controller import AccountPageController

logger = logging.getLogger(__name__)


def delete_ssh_key_dialog(
    account_page_controller: AccountPageController,
    key,
):
    logger.info("Open delete_ssh_key_dialog")

    async def confirm_delete(e):
        await account_page_controller.confirm_delete(
            key,
        )

    return ft.AlertDialog(
        title=ft.Text("Удаление SSH ключа"),
        content=ft.Text(
            f"Вы уверены, что хотите удалить ключ '{key.name}'?\n"
            "Это действие нельзя отменить."
        ),
        actions=[
            ft.TextButton("Отмена", on_click=account_page_controller.pop_dialog),
            ft.FilledButton(
                "Удалить", on_click=confirm_delete, color=ft.Colors.RED_400
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
