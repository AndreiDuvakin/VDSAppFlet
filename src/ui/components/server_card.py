import flet as ft

from src.domain.server import Server


def server_card(server: Server, on_click=None) -> ft.Control:
    return ft.Card(
        elevation=3,
        margin=ft.Margin.only(bottom=12),
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Row(
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
                            ft.Text(
                                f"#{server.ctid}",
                                color=ft.Colors.GREY_500,
                                size=14,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    ft.Divider(height=1),

                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LANGUAGE, color=ft.Colors.BLUE_400),
                            ft.Text("Публичный IP:", color=ft.Colors.GREY_600),
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
                            ft.Icon(ft.Icons.MEMORY, color=ft.Colors.BLUE_GREY_400),
                            ft.Text(
                                server.get_os_name,
                                size=15,
                            ),
                        ],
                        spacing=8,
                    ),

                    ft.Row(
                        [
                            ft.Text(
                                server.get_resources_text,
                                size=15,
                                color=ft.Colors.GREY_700,
                            ),
                        ]
                    ),
                ],
                spacing=10,
            ),
        ),
    )


