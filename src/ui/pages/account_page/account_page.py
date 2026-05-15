from typing import Callable

import flet as ft

from src.services.account_service import AccountService
from src.services.ssh_keys_service import SSHKeysService
from src.state.app_state import AppState
from src.ui.pages.account_page.tabs.notifications_tab import notifications_tab
from src.ui.pages.account_page.tabs.profile_tab import profile_tab
from src.ui.pages.account_page.tabs.ssh_keys_tab import ssh_keys_tab
from src.services.notification_service import NotificationService


def AccountView(
        state: AppState,
        set_state: Callable,
        page: ft.Page,
        account_service: AccountService,
        ssh_keys_service: SSHKeysService,
        notification_service: NotificationService,
) -> ft.Control:
    def on_tab_changed(e):
        state.account_tab_index = e.control.selected_index
        load_current_tab_data(e.control.selected_index)  # ← добавили

    def load_current_tab_data(tab_index: int):
        if tab_index == 0:
            if state.account.info is None and not state.account.loading:
                page.run_task(account_service.load_account, state)

        elif tab_index == 1:
            if not state.ssh_keys.items and not state.ssh_keys.loading:
                page.run_task(ssh_keys_service.load_ssh_keys, state)

        elif tab_index == 2:
            if state.notification.settings is None and not state.notification.loading:
                page.run_task(notification_service.load_settings, state)

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
                                    service=account_service,
                                ),
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ssh_keys_tab(
                                    page=page,
                                    state=state,
                                    service=ssh_keys_service,
                                ),
                                expand=True,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=notifications_tab(
                                    page=page,
                                    state=state,
                                    service=notification_service,
                                ),
                                expand=True,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
