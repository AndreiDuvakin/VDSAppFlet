from dataclasses import dataclass

import flet as ft

from src.state.load_state import LoadState


@dataclass
@ft.observable
class ServerCardState:
    server_loading_status: LoadState = LoadState.IDLE
    is_server_loading: bool = False

    def set_server_loading_status(self, status: LoadState) -> None:
        self.server_loading_status = status

    def set_is_server_loading(self, is_server_loading: bool):
        self.is_server_loading = is_server_loading
