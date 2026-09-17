from dataclasses import dataclass

import flet as ft

from src.models.server import GetServer
from src.state.load_state import LoadState


@dataclass
@ft.observable
class ServerDetailPageState:
    server: GetServer | None = None

    server_loading_status: LoadState = LoadState.IDLE

    is_server_loading: bool = False
    current_tab_index: int = 0

    def set_server_loading_status(self, status: LoadState) -> None:
        self.server_loading_status = status

    def set_current_tab_index(self, index: int) -> None:
        self.current_tab_index = index

    def set_server(self, server: GetServer | None) -> None:
        self.server = server

    def set_is_server_loading(self, is_server_loading: bool) -> None:
        self.is_server_loading = is_server_loading
