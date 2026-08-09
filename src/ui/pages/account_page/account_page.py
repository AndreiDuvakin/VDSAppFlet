import flet as ft

from core.contexts import AppContext
from ui.pages.account_page.tabs.profile_tab import profile_tab


@ft.component
def account_page():
    app_state = ft.use_context(AppContext)

    def on_tab_changed(e):
        pass

    return ft.Tabs(
            selected_index=app_state.account_page_state.current_tab_index,
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
                                content=profile_tab(),
                                expand=True,
                            ),
                            # ft.Container(
                            #     alignment=ft.Alignment.CENTER,
                            #     content=ssh_keys_tab(
                            #         page=page,
                            #         state=state,
                            #         services=services,
                            #     ),
                            #     expand=True,
                            # ),
                            # ft.Container(
                            #     alignment=ft.Alignment.CENTER,
                            #     content=notifications_tab(
                            #         page=page,
                            #         state=state,
                            #         services=services,
                            #     ),
                            #     expand=True,
                            # ),
                        ],
                    ),
                ],
            )
    )
