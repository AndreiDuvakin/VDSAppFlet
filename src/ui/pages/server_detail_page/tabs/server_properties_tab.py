import flet as ft

from core.contexts import ServerDetailPageContext


@ft.component
def server_properties_tab():
    server_detail_page_state = ft.use_context(ServerDetailPageContext)

    return ft.Column(
        [
            ft.Text("Имя хоста и теги", weight=ft.FontWeight.BOLD, size=25),
            ft.Row(
                [
                    ft.Text("Имя хоста:"),
                    ft.Text(server_detail_page_state.server.hostname),
                ],
                spacing=10,
            ),
        ],
        expand=True,
    )
