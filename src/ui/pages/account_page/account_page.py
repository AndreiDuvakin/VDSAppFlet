import flet as ft

from src.controllers.account_page_controller import AccountPageController
from src.core.contexts import AccountPageContext, ApiClientContext
from src.state.account_page_state import AccountPageState
from src.state.load_state import LoadState
from src.ui.components.show_message_banner import show_message_banner
from src.ui.components.show_simple_dialog import show_simple_dialog
from src.ui.pages.account_page.tabs.notifications_tab.notifications_tab import (
    notifications_tab,
)
from src.ui.pages.account_page.tabs.profile_tab import profile_tab
from src.ui.pages.account_page.tabs.ssh_keys_tab.ssh_keys_tab import ssh_keys_tab


@ft.component
def account_page():
    account_page_state, _ = ft.use_state(AccountPageState)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    account_page_controller = AccountPageController(
        account_page_state,
        api_client.notification_service,
        api_client.ssh_keys_service,
        lambda message, is_error=False: show_message_banner(message, page, is_error),
        lambda: page.pop_dialog(),
        lambda title, message: show_simple_dialog(title, ft.Text(message), page),
    )

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
                            content=ssh_keys_tab(account_page_controller),
                            expand=True,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=notifications_tab(account_page_controller),
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
            account_page_state.notifications_loading_status.value
            == LoadState.LOADING.value
            or account_page_state.ssh_keys_loading_status.value
            == LoadState.LOADING.value
        ):
            tabs.disabled = True
            tabs_content.controls.insert(1, ft.ProgressBar())

        return tabs

    return AccountPageContext(account_page_state, build_tabs)
