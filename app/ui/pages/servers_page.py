import flet as ft

from app.services.servers_service import ServersService
from app.state.app_state import AppState


def ServersView(
        state: AppState,
        page: ft.Page,
        service: ServersService,
) -> ft.Control:
    page.title = 'Список серверов'

    if not state.servers.items and not state.servers.loading and not state.servers.error:
        page.run_task(service.load_servers, state)

    if state.servers.loading:
        return ft.Column(
            [ft.ProgressRing()],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    if state.servers.error:
        return ft.Text(f"Ошибка: {state.servers.error}", color="red")
    if not state.servers.items:
        return ft.Text("Серверы не загружены")

    return ft.Column(
        [
            ft.Text("Список серверов", size=20, weight=ft.FontWeight.BOLD),
            *[ft.Text(f"Сервер ID: {s.ctid}") for s in state.servers.items[:5]],
        ],
        spacing=10,
    )
