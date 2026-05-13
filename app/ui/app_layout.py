from typing import Callable

import flet as ft

from api.account_client import AccountClient
from api.servers_client import ServersClient
from app.core.screens import Screen, SCREENS
from app.state.app_state import AppState
from app.ui.pages.account_page import AccountView
from app.ui.pages.servers_page import ServersView
from services.account_service import AccountService
from services.servers_service import ServersService


def AppLayout(
        page: ft.Page,
        state: AppState,
        set_state: Callable,
) -> ft.Control:

    route = page.route.lstrip("/") or Screen.SERVERS.value

    if route == Screen.ACCOUNT.value:
        client = AccountClient(state.token)
        service = AccountService(client, set_state)

        content = AccountView(state=state, page=page, service=service)
    elif route == Screen.SERVERS.value:
        client = ServersClient(state.token)
        service = ServersService(client, set_state)

        content = ServersView(state=state, page=page, service=service)
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
