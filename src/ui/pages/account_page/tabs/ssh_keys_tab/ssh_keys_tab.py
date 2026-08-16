import asyncio
import logging

import flet as ft

from core.contexts import AccountPageContext, ApiClientContext
from ui.components.empty_content import empty_content
from ui.components.show_message_banner import show_message_banner
from ui.pages.account_page.tabs.ssh_keys_tab.dialogs.create_ssh_key_dialog import (
    create_ssh_key_dialog,
)
from ui.pages.account_page.tabs.ssh_keys_tab.dialogs.delete_ssh_key_dialog import (
    delete_ssh_key_dialog,
)

logger = logging.getLogger(__name__)


@ft.component
def ssh_keys_tab():
    logger.info("Initializing ssh keys tab")

    account_page_state = ft.use_context(AccountPageContext)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    def show_create_ssh_key_dialog():
        page.show_dialog(
            create_ssh_key_dialog(
                page=page,
                account_page_state=account_page_state,
                api_client=api_client,
            )
        )

    def show_delete_ssh_key_dialog(key):
        page.show_dialog(
            delete_ssh_key_dialog(
                key=key,
                page=page,
                account_page_state=account_page_state,
                api_client=api_client,
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

    async def get_ssh_keys():
        try:
            logger.info("Trying to get ssh keys")
            account_page_state.set_is_loading_ssh_keys(True)
            ssh_keys_list = await api_client.ssh_keys_service.get_ssh_keys()
            logger.info("SSH keys loaded")
            account_page_state.set_ssh_keys(ssh_keys_list)
        except Exception as e:
            logger.exception(f"Error requesting SSH keys: {str(e)}")
            show_message_banner(
                "Ошибка получения списка SSH ключей.",
                page,
            )

        finally:
            logger.info("Finally loading SSH keys")
            account_page_state.set_is_loading_ssh_keys(False)

    if (
        account_page_state.ssh_keys is None
        and not account_page_state.is_loading_ssh_keys
    ):
        logger.info("SSHE keys not loaded, starting loading")
        asyncio.create_task(get_ssh_keys())

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
                                        on_click=lambda e: show_delete_ssh_key_dialog(
                                            key,
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
