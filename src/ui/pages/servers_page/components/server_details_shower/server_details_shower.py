import flet as ft

from src.domain.server import Server
from src.ui.pages.servers_page.components.server_details_shower.tabs.server_parameters import server_parameters


def show_server_details(page: ft.Page, server: Server):
    selected_index = 0

    def on_tab_change(e):
        nonlocal selected_index
        selected_index = int(e.data)
        content_container.controls[0] = get_content()
        page.update()

    def get_content():
        if selected_index == 0:
            return server_parameters(server)

        elif selected_index == 1:
            return ft.Column([ft.Text("История действий (в разработке)", size=20)], expand=True)

        elif selected_index == 2:
            return ft.Column([ft.Text("Бэкапы (в разработке)", size=20)], expand=True)

        else:
            return ft.Column([ft.Text("Действия (в разработке)", size=20)], expand=True)

    content_container = ft.Column([get_content()], expand=True)

    sheet = ft.BottomSheet(
        fullscreen=True,
        show_drag_handle=True,
        content=ft.Container(
            padding=ft.Padding.all(16),
            content=ft.Column(
                [
                    ft.Row(
                        [
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
            ),
        ),
    )

    page.show_dialog(sheet)
