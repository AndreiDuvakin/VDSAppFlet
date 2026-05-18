import flet as ft

from src.services.servers_service import ServersService
from src.domain.server import Server
from src.state.app_state import AppState


def show_server_actions(
        page: ft.Page,
        server: Server,
        service: ServersService,
        state: AppState,
):
    async def restart_server(e):
        page.pop_dialog()
        await service.restart_server(state, server.ctid)

    async def start_server(e):
        page.pop_dialog()
        await service.start_server(state, server.ctid)

    async def stop_server(e):
        page.pop_dialog()
        await service.stop_server(state, server.ctid)

    actions_sheet = ft.CupertinoActionSheet(
        title=ft.Text(f"{server.name or server.hostname} (#{server.ctid})"),
        message=ft.Text(f"Статус: {server.status_text} • {server.public_ip}"),
        actions=[],
    )

    if server.status == 'started':
        actions_sheet.actions.extend([
            ft.CupertinoActionSheetAction(
                content="Перезагрузить сервер",
                on_click=restart_server,
            ),
            ft.CupertinoActionSheetAction(
                content="Выключить сервер",
                on_click=stop_server,
            ),
        ])

    elif server.status == 'stopped':
        actions_sheet.actions.append(
            ft.CupertinoActionSheetAction(
                content='Запустить',
                on_click=start_server,
            )
        )

    page.show_dialog(ft.CupertinoBottomSheet(actions_sheet))
