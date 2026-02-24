import asyncio

import flet as ft

from app.services.servers_service import ServersService
from app.state.app_state import AppState


@ft.component
def ServersView(state: AppState, service: ServersService) -> ft.Control:
    if state.servers.loading:
        return ft.ProgressRing()

    def refresh_click(e):
        asyncio.create_task(service.load)

    servers_list = []
    for server in state.servers.items:
        servers_list.extend([
            ft.Text(f"{server.name} ({server.hostname})"),
            ft.Text(f"Статус: {server.status} | План: {server.rplan} | Локация: {server.location}"),
            ft.Divider()
        ])

    return ft.Column(
        expand=True,
        controls=[
            ft.Row([ft.ElevatedButton("Обновить", on_click=refresh_click)]),
            ft.Column(servers_list) if servers_list else [ft.Text("Серверы не загружены")],
        ])
