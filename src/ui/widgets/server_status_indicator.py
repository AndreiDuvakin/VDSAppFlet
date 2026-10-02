import flet as ft

from src.models.server import GetServer


@ft.component
def server_status_indicator(
    server: GetServer,
):
    return ft.Container(
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
    )
