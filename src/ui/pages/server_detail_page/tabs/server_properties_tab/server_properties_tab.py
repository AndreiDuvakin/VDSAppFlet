import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.core.contexts import AppContext
from src.core.contexts import ServerDetailPageContext
from src.ui.pages.server_detail_page.tabs.server_properties_tab.dialogs.add_new_ssh_keys_to_server_dialog import (  # noqa: E501
    show_add_new_ssh_keys_to_server_dialog,
)

logger = logging.getLogger(__name__)


@ft.component
def server_properties_tab(
    server_detail_page_controller: ServerDetailPageController,
):
    server_detail_page_state = ft.use_context(ServerDetailPageContext)
    app_state = ft.use_context(AppContext)
    page = ft.context.page

    server_tags = ft.use_memo(
        lambda: app_state.get_tags_by_server_ctid(server_detail_page_state.server.ctid),
        [
            app_state.tags,
            app_state.servers,
            server_detail_page_state.server,
        ],
    )

    async def add_new_ssh_keys_to_server():
        keys = await server_detail_page_controller.check_keys_to_add_into_server()

        if not keys:
            return

        page.show_dialog(
            show_add_new_ssh_keys_to_server_dialog(
                server_detail_page_controller,
                keys,
            )
        )

    return ft.Column(
        [
            ft.Text("Имя хоста и теги", weight=ft.FontWeight.BOLD, size=25),
            ft.Row(
                [
                    ft.Text("Имя хоста:"),
                    ft.Text(server_detail_page_state.server.hostname),
                ],
                spacing=10,
                tooltip="Имя хоста используемое для идентификации сервера внутри сети",
            ),
            ft.Row(
                [
                    ft.Text("Теги:"),
                    *[
                        ft.Chip(
                            label=tag.name,
                            leading=ft.Icon(ft.Icons.TAG),
                        )
                        for tag in server_tags
                    ],
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                tooltip="Теги используются для группировки серверов"
                " и быстрой навигации",
            ),
            ft.Divider(),
            ft.Text("Параметры публичной сети", weight=ft.FontWeight.BOLD, size=25),
            ft.Row(
                [
                    ft.Text("IP-адрес:"),
                    ft.Text(server_detail_page_state.server.public_address.address),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.Text("Маска подсети:"),
                    ft.Text(server_detail_page_state.server.public_address.netmask),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.Text("Шлюз:"),
                    ft.Text(server_detail_page_state.server.public_address.gateway),
                ],
                spacing=10,
            ),
            ft.Divider(),
            ft.Text("SSH-ключи пользователя root", weight=ft.FontWeight.BOLD, size=25),
            ft.ResponsiveRow(
                [
                    ft.Container(
                        col={
                            ft.ResponsiveRowBreakpoint.XS: 12,
                            ft.ResponsiveRowBreakpoint.MD: 6,
                        },
                        content=ft.Button(
                            "Добавить на сервер существующий ключ",
                            icon=ft.Icons.VPN_KEY,
                            expand=True,
                            on_click=add_new_ssh_keys_to_server,
                        ),
                    ),
                    ft.Container(
                        col={
                            ft.ResponsiveRowBreakpoint.XS: 12,
                            ft.ResponsiveRowBreakpoint.MD: 6,
                        },
                        content=ft.OutlinedButton(
                            "Создать новый ключ",
                            icon=ft.Icons.ADD,
                            expand=True,
                            on_click=lambda: page.navigate(
                                "/account/ssh_keys/create_ssh_key"
                            ),
                        ),
                    ),
                ],
                expand=True,
            ),
            *[
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.VPN_KEY,
                                    color=ft.Colors.BLUE_400,
                                    size=24,
                                ),
                                ft.Text(
                                    key.name,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        padding=10,
                    ),
                )
                for key in server_detail_page_state.server.keys
            ],
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
