import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.core.contexts import AppContext, ServerDetailPageContext
from src.ui.components.empty_content import empty_content
from src.ui.widgets.backup_tile import backup_tile


@ft.component
def backups_tab(
    server_detail_page_controller: ServerDetailPageController,
):
    server_detail_page_state = ft.use_context(ServerDetailPageContext)
    app_state = ft.use_context(AppContext)

    backups = ft.use_memo(
        lambda: app_state.get_backups_by_server_ctid(
            server_detail_page_state.server.ctid
        ),
        [server_detail_page_state.server.ctid, app_state.backups],
    )

    if not backups:
        return empty_content(
            ft.Icons.BACKUP,
            "Нет бэкапов для отображения",
            "Возможно вы еще не создавали бэкапы или они не были загружены",
        )

    return ft.Column(
        [
            ft.ListView(
                [
                    ft.Column(
                        [
                            backup_tile(
                                backup,
                                server_detail_page_state.server,
                            ),
                            ft.Divider(),
                        ],
                    )
                    for backup in backups
                ],
                build_controls_on_demand=True,
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
