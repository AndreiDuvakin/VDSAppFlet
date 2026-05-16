import flet as ft

from src.domain.server import Server


def show_server_details(page: ft.Page, server: Server):
    selected_index = 0

    def on_tab_change(e):
        nonlocal selected_index
        selected_index = int(e.data)
        content_container.controls[0] = get_content()
        page.update()

    def get_content():
        if selected_index == 0:
            return ft.Column([
                ft.ListTile(title=ft.Text("Имя сервера"), subtitle=ft.Text(server.name or server.hostname)),
                ft.ListTile(title=ft.Text("CTID"), subtitle=ft.Text(str(server.ctid))),
                ft.ListTile(title=ft.Text("Статус"), subtitle=ft.Text(server.status_text)),
                ft.ListTile(title=ft.Text("Локация"), subtitle=ft.Text(server.location)),
                ft.ListTile(title=ft.Text("Тариф"), subtitle=ft.Text(server.rplan.upper())),
                ft.ListTile(title=ft.Text("IP"), subtitle=ft.Text(server.public_ip)),
            ], scroll=ft.ScrollMode.AUTO, expand=True)

        elif selected_index == 1:
            return ft.Column([ft.Text("Статистика (в разработке)", size=20)], expand=True)

        elif selected_index == 2:
            return ft.Column([ft.Text("История действий (в разработке)", size=20)], expand=True)

        else:
            return ft.Column([ft.Text("Бэкапы (в разработке)", size=20)], expand=True)

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

                    ft.CupertinoSlidingSegmentedButton(
                        selected_index=selected_index,
                        on_change=on_tab_change,
                        controls=[
                            ft.Text("Параметры"),
                            ft.Text("Статистика"),
                            ft.Text("История"),
                            ft.Text("Бэкапы"),
                        ],
                    ),

                    ft.Divider(),

                    content_container,
                ],
                expand=True,
                spacing=15,
            ),
        ),
    )

    page.show_dialog(sheet)
