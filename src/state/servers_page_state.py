from dataclasses import dataclass

import flet as ft

from src.models.tag import GetTag
from src.state.load_state import LoadState


@dataclass
@ft.observable
class ServersPageState:
    servers_loading_status: LoadState = LoadState.IDLE

    selected_tag_index: int = 0
    selected_tag: GetTag = None

    def set_servers_loading_status(self, status: LoadState) -> None:
        self.servers_loading_status = status

    def set_selected_tag(self, tag: GetTag) -> None:
        self.selected_tag = tag

    def set_selected_tag_index(self, index) -> None:
        self.selected_tag_index = index
