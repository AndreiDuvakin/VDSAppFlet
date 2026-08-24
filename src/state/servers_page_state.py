from dataclasses import dataclass

import flet as ft

from src.models.tag import GetTag


@dataclass
@ft.observable
class ServersPageState:
    is_servers_loading: bool = False

    selected_tag_index: int = 0
    selected_tag: GetTag = None

    def set_selected_tag(self, tag: GetTag) -> None:
        self.selected_tag = tag

    def set_selected_tag_index(self, index) -> None:
        self.selected_tag_index = index

    def set_is_servers_loading(self, is_servers_loading: bool) -> None:
        self.is_servers_loading = is_servers_loading
