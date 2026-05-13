from typing import Callable

import flet as ft

from app.core.screens import Screen, SCREENS
from app.state.app_state import AppState
from app.ui.pages.account_page import AccountView
from app.ui.pages.servers_page import ServersView


def AppLayout(
        page: ft.Page,
        state: AppState,
        set_state: Callable,
) -> ft.Control:

    route = page.route.lstrip("/") or Screen.SERVERS.value

    if route == Screen.ACCOUNT.value:
        content = AccountView(state=state, page=page, set_state=set_state)
    elif route == Screen.SERVERS.value:
        content = ServersView(state=state, page=page, set_state=set_state)
    else:
        content = ft.Text("Страница не найдена", size=24, color="red")

    def go_handler(e):
        index = int(e.data)
        screen = SCREENS[index]
        page.go(screen.value)

    def get_index():
        screen_route = str(route).upper()
        member = Screen[screen_route]
        index = list(Screen).index(member)
        return index

    return ft.Column(
        expand=True,
        controls=[
            ft.AppBar(title=ft.Text("Vscale Client")),
            ft.Container(content=content, expand=True),
            ft.NavigationBar(
                selected_index=get_index(),
                on_change=go_handler,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.CLOUD_OUTLINED, label="Серверы"),
                    ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED, label="Аккаунт"),
                ],
            ),
        ]
    )
