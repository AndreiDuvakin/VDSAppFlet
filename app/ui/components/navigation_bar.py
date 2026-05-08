import flet as ft


def navigation_bar(page, selected_index):
    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=lambda e: page.go(["account", "servers"][e.control.selected_index]),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED),
                label="Аккаунт",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.CLOUD_OUTLINED),
                label="Серверы",
            ),
        ],
    ),
