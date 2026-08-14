from dataclasses import dataclass

import flet as ft

from models.server import GetServer


@dataclass
@ft.observable
class ServerDetailPageState:
    server: GetServer | None = None

    is_server_loading: bool = False
    current_tab_index: int = 0

    def set_current_tab_index(self, index: int):
        self.current_tab_index = index

    def set_server(self, server: GetServer | None):
        self.server = server

    def set_is_server_loading(self, is_server_loading: bool):
        self.is_server_loading = is_server_loading
