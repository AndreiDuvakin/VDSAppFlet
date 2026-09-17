import flet as ft

from src.core.contexts import AppContext
from src.core.contexts import ServerDetailPageContext


@ft.component
def server_properties_tab():
    server_detail_page_state = ft.use_context(ServerDetailPageContext)
    app_state = ft.use_context(AppContext)

    server_tags = ft.use_memo(
        lambda: app_state.get_tags_by_server_ctid(server_detail_page_state.server.ctid),
        [
            app_state.tags,
            app_state.servers,
            server_detail_page_state.server,
        ],
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
            ft.Button("Добавить на сервер существующий ключ"),
            ft.Button("Создать новый ключ"),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
