import asyncio
import logging

import flet as ft

from src.controllers.account_page_controller import AccountPageController
from src.core.contexts import AccountPageContext
from src.state.load_state import LoadState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.pages.account_page.tabs.ssh_keys_tab.dialogs.create_ssh_key_dialog import (
    create_ssh_key_dialog,
)
from src.ui.pages.account_page.tabs.ssh_keys_tab.dialogs.delete_ssh_key_dialog import (
    delete_ssh_key_dialog,
)

logger = logging.getLogger(__name__)


@ft.component
def ssh_keys_tab(
    account_page_controller: AccountPageController,
):
    logger.info("Initializing ssh keys tab")

    account_page_state = ft.use_context(AccountPageContext)
    page = ft.context.page

    def show_create_ssh_key_dialog():
        page.show_dialog(
            create_ssh_key_dialog(
                account_page_controller,
            )
        )

    def show_delete_ssh_key_dialog(key):
        page.show_dialog(
            delete_ssh_key_dialog(
                account_page_controller,
                key,
            )
        )

    add_button = ft.Container(
        content=ft.Button(
            "Добавить SSH ключ",
            icon=ft.Icons.ADD,
            on_click=show_create_ssh_key_dialog,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE,
            ),
        ),
        padding=ft.Padding.only(bottom=15),
    )

    if (
        account_page_state.ssh_keys is None
        and account_page_state.ssh_keys_loading_status.value == LoadState.IDLE.value
    ):
        logger.info("SSH keys not loaded, starting loading")
        asyncio.create_task(account_page_controller.get_ssh_keys())

    if account_page_state.ssh_keys_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить SSH ключи",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            account_page_controller.repeat_loading_ssh_keys,
        )

    if not account_page_state.ssh_keys:
        logger.info("SSH keys is loaded, but it is empty")

        empty_content_component = empty_content(
            ft.Icons.VPN_KEY,
            "Нет SSH ключей",
            "Добавьте публичный SSH ключ для доступа к серверам",
        )

        return ft.Column(
            [
                add_button,
                empty_content_component,
            ],
        )

    logger.info("SSH keys loaded and present")

    ssh_keys_list = ft.ListView(
        expand=True,
        spacing=10,
        controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.VPN_KEY,
                                        color=ft.Colors.BLUE_400,
                                        size=24,
                                    ),
                                    ft.Text(
                                        key.name,
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_400,
                                        tooltip="Удалить ключ",
                                        on_click=lambda e, k=key: show_delete_ssh_key_dialog(  # noqa:E501
                                            k
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Divider(height=5, thickness=0.5),
                            ft.Text(f"ID: {key.id}", size=10, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.all(15),
                ),
                elevation=2,
            )
            for key in account_page_state.ssh_keys
        ],
    )

    return ft.Column(
        [add_button, ssh_keys_list],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
