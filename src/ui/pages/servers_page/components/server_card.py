import flet as ft

from src.core.screens import Screen
from src.domain.server import Server
from src.services.app_services import AppServices
from src.state.app_state import AppState
from src.ui.components.progress_ring import progress_ring
from src.ui.pages.servers_page.components.server_actions_shower import show_server_actions


def server_card(
        page: ft.Page,
        server: Server,
        services: AppServices,
        state: AppState,
) -> ft.Control:
    is_server_in_updating = server.ctid in state.servers.updating_servers_ctids or state.ssh_keys.loading

    async def open_details(e):
        if is_server_in_updating:
            return
        page.go(Screen.server_details(server.ctid))

    def open_actions_menu(e):
        if is_server_in_updating:
            return

        show_server_actions(page, server, services, state)

    card_content = ft.GestureDetector(
        on_tap=open_details,
        content=ft.Card(
            elevation=3,
            margin=ft.Margin.only(bottom=12),
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=progress_ring() if is_server_in_updating else None,
                                            visible=is_server_in_updating,
                                        ),
                                        ft.Container(
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.CIRCLE, color=server.status_color, size=12),
                                                    ft.Text(server.status_text, color=server.status_color,
                                                            weight=ft.FontWeight.W_500),
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
                                        ft.Text(f"#{server.ctid}", color=ft.Colors.GREY_500, size=14),
                                        ft.IconButton(
                                            icon=ft.Icons.MORE_VERT,
                                            on_click=open_actions_menu,
                                        ),
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),

                        ft.Divider(height=1),

                        ft.Row([ft.Icon(ft.Icons.LANGUAGE, color=ft.Colors.BLUE_400),
                                ft.Text("Публичный IP:", color=ft.Colors.GREY_600),
                                ft.Text(server.public_ip, weight=ft.FontWeight.W_500, expand=True)], spacing=8),

                        ft.Row([
                            ft.Icon(ft.Icons.MEMORY, color=ft.Colors.BLUE_GREY_400),
                            ft.Text(server.get_resources_text, size=15)
                        ], spacing=8),

                        ft.Row([ft.Text(server.get_resources_text, size=15, color=ft.Colors.GREY_700)]),
                    ],
                    spacing=10,
                ),
            ),
        )
    )

    return ft.Container(
        content=card_content,
        disabled=is_server_in_updating,
    )
