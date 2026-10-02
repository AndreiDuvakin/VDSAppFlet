import flet as ft

from src.controllers.backup_tile_controller import BackupTileController
from src.core.constants import DEFAULT_ISO_IMAGE
from src.core.contexts import ApiClientContext, AppContext
from src.models.backup import GetBackup
from src.models.server import GetServer
from src.state.backup_tile_state import BackupTileState
from src.state.load_state import LoadState
from src.ui.components.show_message_banner import show_message_banner
from src.ui.widgets.backup_tile.dialogs.delete_backup_dialog import delete_backup_dialog


@ft.component
def backup_tile(
    backup: GetBackup,
    server: GetServer | None = None,
):
    backup_tile_state, _ = ft.use_state(BackupTileState)
    app_state = ft.use_context(AppContext)
    api_client = ft.use_context(ApiClientContext)
    resolved_server = server
    page = ft.context.page

    backup_tile_controller = BackupTileController(
        api_client.backups_service,
        backup_tile_state,
        app_state,
        lambda message, is_error=False: show_message_banner(message, page, is_error),
        lambda: page.pop_dialog(),
    )

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

    def show_delete_backup_dialog(e):
        page.show_dialog(
            delete_backup_dialog(
                backup_tile_controller,
                backup,
            )
        )

    is_loading_status = (
        backup_tile_state.backup_loading_status.value == LoadState.LOADING.value
    )

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
                on_click=show_delete_backup_dialog,
            ),
        ],
        content=ft.IconButton(
            icon=ft.Icons.MORE_VERT,
            on_click=open_menu,
        ),
    )

    row_content = ft.Row(
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
        disabled=is_loading_status,
    )

    if not is_loading_status:
        page_content = row_content

    else:
        page_content = ft.Column(
            [
                ft.ProgressBar(),
                row_content,
            ],
            expand=True,
        )

    return ft.Card(
        content=ft.Container(
            content=page_content,
            padding=10,
        ),
    )
