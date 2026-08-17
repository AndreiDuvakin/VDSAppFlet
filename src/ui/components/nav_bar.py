import flet as ft

from src.ui.components.nav_link import nav_link


@ft.component
def nav_bar():
    return ft.Container(
        content=ft.Row(
            [
                nav_link(ft.Icons.HOME, "/servers", "Серверы"),
                nav_link(ft.Icons.ACCOUNT_CIRCLE, "/account", "Аккаунт"),
                nav_link(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    "/billing",
                    "Баланс",
                ),
                nav_link(
                    ft.Icons.INFO,
                    "/info",
                    "Информация",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.Colors.SURFACE_BRIGHT,
        padding=10,
        border_radius=15,
    )
