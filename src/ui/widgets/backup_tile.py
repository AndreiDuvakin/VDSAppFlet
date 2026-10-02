import flet as ft

from src.core.constants import DEFAULT_ISO_IMAGE
from src.core.contexts import AppContext
from src.models.backup import GetBackup
from src.models.server import GetServer


@ft.component
def backup_tile(
    backup: GetBackup,
    server: GetServer | None = None,
):
    app_state = ft.use_context(AppContext)
    resolved_server = server

    if resolved_server is None:
        resolved_server = ft.use_memo(
            lambda: app_state.get_server_by_id(backup.scalet),
            [server, backup.scalet, app_state.servers],
        )

    if resolved_server is None:
        return ft.Row(
            [
                ft.Image(
                    DEFAULT_ISO_IMAGE,
                    width=40,
                    height=40,
                ),
                ft.Text("Сервер бэкапа не найден"),
            ],
        )

    async def open_menu(e):
        await menu.open()

    menu = ft.ContextMenu(
        items=[
            ft.PopupMenuItem(
                icon=ft.Icons.SETTINGS_BACKUP_RESTORE,
                content=ft.Text(
                    "Восстановить сервер",
                ),
            ),
            ft.PopupMenuItem(
                icon=ft.Icons.COMPUTER,
                content=ft.Text(
                    "Создать сервер",
                ),
            ),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(
                icon=ft.Icons.DELETE,
                content=ft.Text(
                    "Удалить бэкап",
                ),
            ),
        ],
        content=ft.IconButton(
            icon=ft.Icons.MORE_VERT,
            on_click=open_menu,
        ),
    )

    return ft.Row(
        [
            ft.Image(
                resolved_server.iso_image,
                width=40,
                height=40,
            ),
            ft.Row(
                [
                    ft.Text(
                        backup.name,
                    ),
                    ft.Text(
                        backup.created,
                    ),
                    ft.Text(
                        resolved_server.plan_description,
                    ),
                    ft.Text(
                        resolved_server.beautiful_location,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=True,
            ),
            menu,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
