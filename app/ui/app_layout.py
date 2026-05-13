from typing import Callable

import flet as ft

from api.ssh_keys_client import SSHKeysClient
from app.api.account_client import AccountClient
from app.api.servers_client import ServersClient
from app.core.screens import Screen, SCREENS
from app.state.app_state import AppState
from app.ui.pages.servers_page import ServersView
from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.ui.pages.account_page.account_page import AccountView
from services.ssh_keys_service import SSHKeysService


def AppLayout(
        page: ft.Page,
        state: AppState,
        set_state: Callable,
) -> ft.Control:

    route = page.route.lstrip("/") or Screen.SERVERS.value

    if route == Screen.ACCOUNT.value:
        account_client = AccountClient(state.token)
        account_service = AccountService(account_client, set_state)

        ssh_keys_client = SSHKeysClient(state.token)
        ssh_keys_service = SSHKeysService(ssh_keys_client, set_state)

        content = AccountView(state=state, page=page, account_service=account_service, ssh_keys_service=ssh_keys_service)
    elif route == Screen.SERVERS.value:
        servers_client = ServersClient(state.token)
        servers_service = ServersService(servers_client, set_state)

        content = ServersView(state=state, page=page, service=servers_service)
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
            ft.AppBar(title=ft.Text("VDS Selectel - Неофициальный клиент")),
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
