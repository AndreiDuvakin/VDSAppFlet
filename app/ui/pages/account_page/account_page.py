import flet as ft

from app.services.account_service import AccountService
from app.state.app_state import AppState
from app.ui.pages.account_page.tabs.profile_tab import profile_tab
from services.ssh_keys_service import SSHKeysService
from ui.pages.account_page.tabs.ssh_keys_tab import ssh_keys_tab


def AccountView(state: AppState, page: ft.Page, account_service: AccountService, ssh_keys_service: SSHKeysService) -> ft.Control:
    return ft.SafeArea(
        expand=True,
        content=ft.Tabs(
            selected_index=0,
            length=2,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Профиль", icon=ft.Icons.PERSON),
                            ft.Tab(label="SSH ключи", icon=ft.Icons.KEY),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=profile_tab(
                                    page=page,
                                    state=state,
                                    service=account_service,
                                ),
                                padding=20,
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ssh_keys_tab(
                                    page=page,
                                    state=state,
                                    service=ssh_keys_service,
                                ),
                                padding=20,
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text("This is Tab 3"),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
