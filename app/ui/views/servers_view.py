import asyncio

import flet as ft

from app.services.servers_service import ServersService
from app.state.app_state import AppState


@ft.component
def ServersView(state: AppState, service: ServersService) -> ft.Control:

    return ft.Column(
        expand=True,
        controls=[

        ])
