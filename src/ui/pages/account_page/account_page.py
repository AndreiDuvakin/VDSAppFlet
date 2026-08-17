import flet as ft

from src.core.contexts import AccountPageContext
from src.state.account_page_state import AccountPageState
from src.ui.pages.account_page.tabs.notifications_tab.notifications_tab import (
    notifications_tab,
)
from src.ui.pages.account_page.tabs.profile_tab import profile_tab
from src.ui.pages.account_page.tabs.ssh_keys_tab.ssh_keys_tab import ssh_keys_tab


@ft.component
def account_page():
    account_page_state, _ = ft.use_state(AccountPageState)

    def on_tab_changed(e):
        account_page_state.set_current_tab_index(e.control.selected_index)

    def build_tabs():
        tabs_content = ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Профиль", icon=ft.Icons.PERSON),
                        ft.Tab(label="SSH ключи", icon=ft.Icons.KEY),
                        ft.Tab(
                            label="Настройка уведомлений", icon=ft.Icons.NOTIFICATIONS
                        ),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=profile_tab(),
                            expand=True,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=ssh_keys_tab(),
                            expand=True,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=notifications_tab(),
                            expand=True,
                        ),
                    ],
                ),
            ],
        )
        tabs = ft.Tabs(
            selected_index=account_page_state.current_tab_index,
            on_change=on_tab_changed,
            length=3,
            expand=True,
            content=tabs_content,
        )

        if (
            account_page_state.is_loading_ssh_keys
            or account_page_state.is_loading_notifications
        ):
            tabs.disabled = True
            tabs_content.controls.insert(1, ft.ProgressBar())

        return tabs

    return AccountPageContext(account_page_state, build_tabs)
