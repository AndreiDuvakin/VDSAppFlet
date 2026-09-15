import logging

import flet as ft

from src.controllers.account_page_controller import AccountPageController

logger = logging.getLogger(__name__)


def create_ssh_key_dialog(
    account_page_controller: AccountPageController,
):
    logger.info("open create_ssh_key_dialog")

    name_field = ft.TextField(
        label="Название ключа",
        hint_text="Например: Мой домашний ПК",
        max_length=255,
    )
    key_field = ft.TextField(
        label="Публичный ключ",
        hint_text="ssh-rsa AAAAB3NzaC1yc2E...",
        multiline=True,
        min_lines=3,
        max_lines=10,
    )

    async def add_key(e):
        await account_page_controller.add_key(
            name_field.value,
            key_field.value,
        )

    return ft.AlertDialog(
        title=ft.Text("Добавление SSH ключа"),
        content=ft.Column(
            [
                ft.Text("Добавьте новый публичный SSH ключ для доступа к серверам."),
                ft.Divider(),
                name_field,
                key_field,
            ],
            spacing=15,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        ),
        actions=[
            ft.TextButton("Отмена", on_click=account_page_controller.pop_dialog),
            ft.FilledButton(
                "Добавить",
                on_click=add_key,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
