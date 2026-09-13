import logging
from typing import Callable

import flet as ft

from src.controllers.servers_page.server_card_controller import ServerCardController
from src.core.contexts import ApiClientContext, AppContext
from src.models.server import GetServer
from src.state.load_state import LoadState
from src.state.server_card_state import ServerCardState
from src.ui.components.show_message_banner import show_message_banner

logger = logging.getLogger(__name__)


@ft.component
def server_card(
    server: GetServer,
    refresh_servers: Callable,
):
    server_card_state, _ = ft.use_state(ServerCardState)
    api_client = ft.use_context(ApiClientContext)
    app_state = ft.use_context(AppContext)
    page = ft.context.page

    def open_details(e):
        page.navigate(f"/server/{server.ctid}")

    async def open_menu(e):
        await menu.open()

    server_card_controller = ServerCardController(
        server_card_state,
        api_client.servers_service,
        app_state,
        server,
        refresh_servers,
        lambda message: show_message_banner(message, page, False),
        lambda message: show_message_banner(message, page),
    )

    menu = ft.ContextMenu(
        items=[],
        content=ft.IconButton(
            icon=ft.Icons.MORE_VERT,
            on_click=open_menu,
        ),
    )

    if server.is_power_on:
        menu.items.extend(
            [
                ft.PopupMenuItem(
                    icon=ft.Icons.AUTORENEW,
                    content="Перезагрузить",
                    on_click=server_card_controller.restart_server,
                ),
                ft.PopupMenuItem(
                    icon=ft.Icons.POWER_SETTINGS_NEW,
                    content="Выключить",
                    on_click=server_card_controller.stop_server,
                ),
            ]
        )

    else:
        menu.items.extend(
            [
                ft.PopupMenuItem(
                    icon=ft.Icons.POWER_SETTINGS_NEW,
                    content="Включить",
                    on_click=server_card_controller.start_server,
                ),
            ]
        )

    if app_state.price is None:
        price_block = ft.ProgressRing()

    else:
        price = app_state.price.get_month_price_beautiful(server.rplan)

        if price is None:
            price_block = ft.ProgressRing()

        else:
            price_block = ft.Text(price, size=15)

    plan_description = ft.Row(
        [
            ft.Text(server.plan_description, size=15),
            price_block,
        ]
    )

    card_column = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.CIRCLE,
                                            color=server.status_color,
                                            size=12,
                                        ),
                                        ft.Text(
                                            server.status_text,
                                            color=server.status_color,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ),
                            ft.Text(
                                server.name or server.hostname,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"#{server.ctid}", color=ft.Colors.GREY_500, size=14
                            ),
                            menu,
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            (
                ft.Divider(height=1)
                if (
                    not server_card_state.server_loading_status.value
                    == LoadState.LOADING.value
                    and server.status != "queued"
                )
                else ft.ProgressBar()
            ),
            ft.Row(
                [
                    ft.Image(
                        server.iso_image,
                        width=50,
                        height=50,
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.LANGUAGE, color=ft.Colors.BLUE_400
                                    ),
                                    ft.Text("Публичный IP:"),
                                    ft.Text(
                                        server.public_ip,
                                        weight=ft.FontWeight.W_500,
                                        expand=True,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.SETTINGS_SYSTEM_DAYDREAM,
                                        color=ft.Colors.CYAN_400,
                                    ),
                                    ft.Text(
                                        server.beautiful_name,
                                        weight=ft.FontWeight.W_500,
                                        expand=True,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.MEMORY, color=ft.Colors.BLUE_GREY_400
                                    ),
                                    plan_description,
                                ],
                                spacing=8,
                            ),
                        ]
                    ),
                ]
            ),
        ],
        spacing=10,
    )

    card_content = ft.GestureDetector(
        on_tap=open_details,
        content=ft.Card(
            elevation=3,
            margin=ft.Margin.only(bottom=12),
            content=ft.Container(
                padding=16,
                content=card_column,
            ),
        ),
    )

    return ft.Container(
        content=card_content,
        disabled=server_card_state.is_server_loading,
    )
