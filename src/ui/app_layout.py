import flet as ft

from src.core.screens import Screen, SCREENS
from src.services.app_services import AppServices
from src.state.app_state import AppState
from src.ui.pages.account_page.account_page import account_page
from src.ui.pages.servers_page.servers_page import servers_page
from src.ui.pages.server_details_page.server_details_page import server_details_page


def AppLayout(
        page: ft.Page,
        state: AppState,
        services: AppServices,
) -> ft.Control:
    route = page.route.lstrip("/") or Screen.SERVERS.value
    is_navigation_visible = True

    server_ctid = Screen.parse_server_route(page.route)
    if server_ctid is not None:
        is_navigation_visible = False
        content = server_details_page(
            page=page,
            services=services,
            state=state,
            ctid=server_ctid,
        )
    elif route == Screen.ACCOUNT.value:
        content = account_page(
            state=state,
            page=page,
            services=services,
        )
    elif route == Screen.SERVERS.value:
        content = servers_page(
            state=state,
            page=page,
            services=services,
        )
    else:
        content = ft.Text("Страница не найдена", size=24, color="red")

    if is_navigation_visible:
        def go_handler(e):
            index = int(e.data)
            screen = SCREENS[index]
            page.go(screen.value)

        def get_index():
            screen_route = str(route).upper()
            member = Screen[screen_route]
            index = list(Screen).index(member)
            return index

        navigation = ft.Container(
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
        )

    else:
        navigation = ft.Container()

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                content=content,
                expand=True,
                margin=ft.Margin.only(top=30)
            ),

            navigation,
        ]
    )
