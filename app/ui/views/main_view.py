import flet as ft

from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.state.app_state import AppState
from app.ui.views.account_view import AccountView
from app.ui.views.servers_view import ServersView


@ft.component
def MainView(
    state: AppState,
    account_service: AccountService,
    servers_service: ServersService,
    page: ft.Page,
) -> list[ft.Control]:

    def tab_changed(e):
        state.current_tab = e.control.selected_index

    tabs = [
        ft.Tab("Аккаунт", ),
        ft.Tab("Серверы", )
    ]

    return [
        ft.AppBar(title=ft.Text("Vscale Client")),
        ft.Tabs(
            selected_index=state.current_tab,
            length=3,
            on_change=tab_changed,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=tabs,
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            AccountView(state, account_service, page),
                            ServersView(state, servers_service),
                        ],
                    ),
                ]
            ),
        ),
    ]
