from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class ServersPageState:
    is_servers_loading: bool = False

    def set_is_servers_loading(self, is_servers_loading: bool):
        self.is_servers_loading = is_servers_loading
