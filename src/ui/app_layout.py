from typing import Callable

import flet as ft

from src.api.notification_client import NotificationClient
from src.api.ssh_keys_client import SSHKeysClient
from src.api.account_client import AccountClient
from src.api.servers_client import ServersClient
from src.core.screens import Screen, SCREENS
from src.state.app_state import AppState
from src.ui.pages.servers_page import ServersView
from src.services.account_service import AccountService
from src.services.servers_service import ServersService
from src.ui.pages.account_page.account_page import AccountView
from src.services.notification_service import NotificationService
from src.services.ssh_keys_service import SSHKeysService


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

        notification_client = NotificationClient(state.token)
        notification_service = NotificationService(notification_client, set_state)

        content = AccountView(
            state=state,
            set_state=set_state,
            page=page,
            account_service=account_service,
            ssh_keys_service=ssh_keys_service,
            notification_service=notification_service,
        )
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
            ft.Container(
                content=content,
                expand=True,
            ),

            ft.Container(
                alignment=ft.Alignment.BOTTOM_CENTER,
                content=ft.Container(
                    content=ft.NavigationBar(
                        selected_index=get_index(),
                        on_change=go_handler,
                        destinations=[
                            ft.NavigationBarDestination(
                                icon=ft.Icons.CLOUD_OUTLINED,
                                label="Серверы"
                            ),
                            ft.NavigationBarDestination(
                                icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                                label="Аккаунт"
                            ),
                        ],
                        bgcolor=ft.Colors.WHITE,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(16),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,

                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.BLACK.with_opacity(0.1, ft.Colors.WHITE),
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ),
        ]
    )
