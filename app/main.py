import os
import flet as ft
from dotenv import load_dotenv

from app.api.servers_client import ServersClient
from app.api.account_client import AccountClient
from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.state.app_state import AppState
from app.ui.pages.account_page import AccountView
from app.ui.pages.servers_page import ServersView


def main(page: ft.Page):
    load_dotenv()
    page.title = "Vscale Client"
    page.theme_mode = ft.ThemeMode.SYSTEM

    token = os.environ.get('TOKEN')
    if not token:
        page.add(ft.Text("TOKEN не найден", color="red"))
        return

    account_client = AccountClient(token)
    servers_client = ServersClient(token)

    state = AppState()

    def set_state(new_state):
        nonlocal state
        state = new_state
        render_page()

    account_service = AccountService(account_client, set_state)
    servers_service = ServersService(servers_client, set_state)

    def render_page():
        page.clean()
        route = page.route.lstrip("/") or "account"

        if route == "account":
            content = AccountView(state, account_service, page)
        elif route == "servers":
            content = ServersView(state, servers_service, page)
        else:
            content = ft.Text("Страница не найдена", size=24, color="red")

        selected_index = 0 if route == "account" else 1

        layout = ft.Column(
            expand=True,
            controls=[
                ft.AppBar(title=ft.Text("Vscale Client")),
                ft.Container(content=content, expand=True),
                ft.NavigationBar(
                    selected_index=selected_index,
                    on_change=lambda e: page.go(["account", "servers"][e.control.selected_index]),
                    destinations=[
                        ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED, label="Аккаунт"),
                        ft.NavigationBarDestination(icon=ft.Icons.CLOUD_OUTLINED, label="Серверы"),
                    ],
                ),
            ]
        )
        page.add(layout)
        page.update()

    def on_route_change(e: ft.RouteChangeEvent):
        render_page()

    page.on_route_change = on_route_change
    if not page.route:
        page.go("/account")
    else:
        render_page()


ft.run(main)