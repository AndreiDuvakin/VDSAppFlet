import flet as ft

from src.core.screens import Screen
from src.services.app_services import AppServices
from src.state.app_state import AppState
from src.ui.components.show_simple_dialog import show_simple_dialog
from src.ui.pages.server_details_page.tabs.server_parameters.server_parameters import server_parameters
from src.ui.components.progress_ring import progress_ring


def server_details_page(
        page: ft.Page,
        services: AppServices,
        state: AppState,
        ctid: int,
):
    server = next((s for s in state.servers.items if s.ctid == ctid), None)
    if server is None:
        show_simple_dialog(
            'Внимание',
            ft.Text(f'Не удалось найти сервер с ID {str(ctid)}', size=20, weight=ft.FontWeight.BOLD),
            page,
        )
        page.go('/')
        return ft.Column([])

    if state.servers.loading:
        return progress_ring()

    if state.servers.error:
        page.pop_dialog()
        page.go('/')
        return ft.Column([])

    selected_index = 0

    def on_tab_change(e):
        nonlocal selected_index
        selected_index = int(e.data)
        content_container.controls[0] = get_content()
        page.update()

    def get_content():
        if selected_index == 0:
            return server_parameters(server, services, state, page)

        elif selected_index == 1:
            return ft.Column([ft.Text("История действий (в разработке)", size=20)], expand=True)

        elif selected_index == 2:
            return ft.Column([ft.Text("Бэкапы (в разработке)", size=20)], expand=True)

        else:
            return ft.Column([ft.Text("Действия (в разработке)", size=20)], expand=True)

    content_container = ft.Column([get_content()], expand=True)

    sheet = ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: page.go(Screen.SERVERS.value),
                    ),
                    ft.Text("Сервер", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"#{server.ctid}", color=ft.Colors.GREY_500),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.CupertinoSlidingSegmentedButton(
                        selected_index=selected_index,
                        on_change=on_tab_change,
                        controls=[
                            ft.Text("Параметры"),
                            ft.Text("История"),
                            ft.Text("Бэкапы"),
                            ft.Text("Действия"),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),

            content_container,
        ],
        expand=True,
        spacing=15,
    )

    return sheet
