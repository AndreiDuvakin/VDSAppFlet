import flet as ft

from src.ui.components.nav_link import nav_link


@ft.component
def nav_bar():
    return ft.Container(
        content=ft.Row(
            [
                nav_link(ft.Icons.HOME, "/servers"),
                nav_link(ft.Icons.TAG, "/tags"),
                nav_link(ft.Icons.ACCOUNT_CIRCLE, "/account"),
                nav_link(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    "/billing",
                ),
                nav_link(
                    ft.Icons.INFO,
                    "/info",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.Colors.SURFACE_BRIGHT,
        padding=10,
        border_radius=15,
    )
