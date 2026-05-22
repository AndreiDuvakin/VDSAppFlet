import flet as ft

from src.services.app_services import AppServices
from src.state.app_state import AppState
from src.ui.pages.account_page.tabs.notifications_tab import notifications_tab
from src.ui.pages.account_page.tabs.profile_tab import profile_tab
from src.ui.pages.account_page.tabs.ssh_keys_tab import ssh_keys_tab


def account_page(
        state: AppState,
        page: ft.Page,
        services: AppServices,
) -> ft.Control:
    def on_tab_changed(e):
        state.account_tab_index = e.control.selected_index
        load_current_tab_data(e.control.selected_index)  # ← добавили

    def load_current_tab_data(tab_index: int):
        if tab_index == 0:
            if state.account.info is None and not state.account.loading:
                page.run_task(services.account_service.load_account, state)

        elif tab_index == 1:
            if not state.ssh_keys.items and not state.ssh_keys.loading:
                page.run_task(services.ssh_keys_service.load_ssh_keys, state)

        elif tab_index == 2:
            if state.notification.settings is None and not state.notification.loading:
                page.run_task(services.notification_service.load_settings, state)

    load_current_tab_data(state.account_tab_index)

    return ft.SafeArea(
        expand=True,
        content=ft.Tabs(
            selected_index=state.account_tab_index,
            on_change=on_tab_changed,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Профиль", icon=ft.Icons.PERSON),
                            ft.Tab(label="SSH ключи", icon=ft.Icons.KEY),
                            ft.Tab(label="Настройка уведомлений", icon=ft.Icons.NOTIFICATIONS),
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
                                    services=services,
                                ),
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ssh_keys_tab(
                                    page=page,
                                    state=state,
                                    services=services,
                                ),
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=notifications_tab(
                                    page=page,
                                    state=state,
                                    services=services,
                                ),
                                expand=True,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
