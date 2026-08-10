import flet as ft

from ui.components.nav_link import nav_link


@ft.component
def nav_bar():
    return ft.Container(
        content=ft.Row(
            [
                nav_link(
                    ft.Icons.HOME,
                    "/servers",
                ),
                nav_link(
                    ft.Icons.ACCOUNT_CIRCLE,
                    "/account",
                ),
                nav_link(
                    ft.Icons.INFO_OUTLINE,
                    "/info",
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.Colors.SURFACE_BRIGHT,
        padding=10,
        border_radius=15,
    )
