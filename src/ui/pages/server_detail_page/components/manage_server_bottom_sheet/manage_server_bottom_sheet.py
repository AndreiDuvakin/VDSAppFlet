import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.ui.pages.server_detail_page.components.manage_server_bottom_sheet.dialogs.create_backup_server_dialog import (  # noqa: E501
    create_backup_server_dialog,
)
from src.ui.pages.server_detail_page.components.manage_server_bottom_sheet.dialogs.delete_server_dialog import (  # noqa: E501
    delete_server_dialog,
)
from src.ui.pages.server_detail_page.components.manage_server_bottom_sheet.dialogs.rebuild_server_dialog import (  # noqa: E501
    rebuild_server_dialog,
)


def manage_server_bottom_sheet(
    server_detail_page_controller: ServerDetailPageController,
):
    server = server_detail_page_controller.server_detail_page_state.server
    controls = []

    def show_rebuild_server_dialog(e: ft.Event[ft.Button]) -> None:
        server_detail_page_controller.show_page_dialog(
            rebuild_server_dialog(
                server_detail_page_controller,
            )
        )

    def show_delete_server_dialog(e: ft.Event[ft.Button]) -> None:
        server_detail_page_controller.show_page_dialog(
            delete_server_dialog(
                server_detail_page_controller,
            )
        )

    def show_create_server_backup_dialog(e: ft.Event[ft.Button]) -> None:
        server_detail_page_controller.show_page_dialog(
            create_backup_server_dialog(
                server_detail_page_controller,
            )
        )

    if server.is_power_on:
        controls.extend(
            [
                ft.Row(
                    [
                        ft.Button(
                            "Выключить",
                            icon=ft.Icons.POWER_SETTINGS_NEW,
                            expand=True,
                            on_click=server_detail_page_controller.stop_server,
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Button(
                            "Перезагрузить",
                            icon=ft.Icons.AUTORENEW,
                            expand=True,
                            on_click=server_detail_page_controller.restart_server,
                        ),
                    ],
                ),
            ]
        )

    else:
        controls.append(
            ft.Row(
                [
                    ft.Button(
                        "Включить",
                        icon=ft.Icons.POWER_SETTINGS_NEW,
                        expand=True,
                        on_click=server_detail_page_controller.start_server,
                    ),
                ],
            ),
        )

    controls.extend(
        [
            ft.Divider(),
            ft.Row(
                [
                    ft.Button(
                        "Переустановить",
                        icon=ft.Icons.REPLAY_OUTLINED,
                        expand=True,
                        on_click=show_rebuild_server_dialog,
                    ),
                ],
            ),
            ft.Row(
                [
                    ft.Button(
                        "Создать бэкап",
                        icon=ft.Icons.ADJUST,
                        expand=True,
                        on_click=show_create_server_backup_dialog,
                    ),
                ],
            ),
            ft.Row(
                [
                    ft.Button(
                        "Удалить сервер",
                        icon=ft.Icons.DELETE,
                        expand=True,
                        on_click=show_delete_server_dialog,
                    ),
                ],
            ),
        ]
    )

    return ft.BottomSheet(
        show_drag_handle=True,
        content=ft.Container(
            content=ft.Column(
                controls,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
        ),
    )
