import flet as ft

from src.services.app_services import AppServices
from src.domain.server import Server
from src.state.app_state import AppState
from src.ui.pages.server_details_page.tabs.server_parameters.components.select_ssh_key_to_add import \
    select_ssh_key_to_add


def server_parameters(
        server: Server,
        services: AppServices,
        state: AppState,
        page: ft.Page,
):
    ssh_keys_list = ft.ListView(
        expand=True,
        spacing=10,
        controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VPN_KEY, color=ft.Colors.BLUE_400, size=24),
                                    ft.Text(key.name, size=16, weight=ft.FontWeight.BOLD, expand=True),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Divider(height=5, thickness=0.5),
                            ft.Text(f"ID: {key.id}", size=10, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.all(15),
                ),
                elevation=2,
            ) for key in server.keys
        ],
    )

    return ft.Column([
        ft.Text("Информация о сервере:", weight=ft.FontWeight.W_600),
        ft.ListTile(title=ft.Text("Имя сервера"), subtitle=ft.Text(server.name or server.hostname)),
        ft.ListTile(title=ft.Text("CTID"), subtitle=ft.Text(str(server.ctid))),
        ft.ListTile(title=ft.Text("Статус"), subtitle=ft.Text(server.status_text)),
        ft.ListTile(title=ft.Text("Локация"), subtitle=ft.Text(server.location)),
        ft.ListTile(title=ft.Text("Тариф"), subtitle=ft.Text(server.rplan.upper())),
        ft.ListTile(title=ft.Text("IP"), subtitle=ft.Text(server.public_ip)),
        ft.Divider(height=1),
        ft.Text("SSH-ключи пользователя root:", weight=ft.FontWeight.W_600),
        ft.ResponsiveRow(
            controls=[
                ft.FilledButton(
                    "Добавить новый",
                    icon=ft.Icons.CREATE,
                    col={"xs": 12, "md": 6},
                    bgcolor=ft.Colors.BLUE_600,
                ),
                ft.FilledTonalButton(
                    "Выбрать существующий",
                    icon=ft.Icons.ADD,
                    col={"xs": 12, "md": 6},
                    on_click=lambda e: select_ssh_key_to_add(server, services, state, page),
                ),
            ],
            spacing=12,
        ),
        ssh_keys_list,
    ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
