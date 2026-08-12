from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class ServerCardState:
    is_server_loading: bool = False

    def set_is_server_loading(self, is_server_loading: bool):
        self.is_server_loading = is_server_loading
