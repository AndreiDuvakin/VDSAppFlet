import logging

import flet as ft

from models.ssh_key import PostSSHKey
from ui.components.show_message_banner import show_message_banner
from ui.components.show_simple_dialog import show_simple_dialog

logger = logging.getLogger(__name__)


def create_ssh_key_dialog(page, account_page_state, api_client):
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

    def pop_dialog():
        page.pop_dialog()

    async def add_key(e):
        logger.info("starting ssh key creation")

        name = name_field.value.strip()
        key = key_field.value.strip()

        if not name:
            logger.warning("ssh key name field is empty")
            show_simple_dialog(
                "Внимание",
                ft.Text("Введите название ключа"),
                page,
            )
            return

        if not key:
            logger.warning("ssh key key field is empty")
            show_simple_dialog(
                "Внимание",
                ft.Text("Введите публичный ключ"),
                page,
            )
            return

        if not key.startswith(("ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp")):
            logger.warning("ssh key is not valid")
            show_simple_dialog(
                "Внимание",
                ft.Text("Неверный формат публичного ключа"),
                page,
            )
            return

        try:
            logger.debug("Trying to create ssh key")
            account_page_state.set_is_loading_ssh_keys(True)

            new_key = PostSSHKey(
                name=name,
                key=key,
            )

            pop_dialog()
            new_key = await api_client.ssh_keys_service.create_ssh_key(new_key)

        except Exception as e:  # noqa: F841
            logger.error(f"Error creating ssh key: {e}")
            show_message_banner(
                "Ошибка при добавлении ключа",
                page,
            )

        else:
            logger.info("SSH key successfully created")
            account_page_state.append_ssh_key(new_key)
            show_message_banner(
                "Новый ключ успешно добавлен",
                page,
                is_error=False,
            )

        finally:
            logger.info("Finished creating ssh key")
            account_page_state.set_is_loading_ssh_keys(False)

    dialog = ft.AlertDialog(
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
            ft.TextButton("Отмена", on_click=pop_dialog),
            ft.FilledButton(
                "Добавить",
                on_click=add_key,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog
