from dataclasses import dataclass, field

import flet as ft

from src.models.server import GetServer, GetServerLog
from src.models.ssh_key import GetSSHKey
from src.state.load_state import LoadState


@dataclass
@ft.observable
class ServerDetailPageState:
    server: GetServer | None = None
    ssh_keys_list: list[GetSSHKey] | None = None
    server_logs_list: list[GetServerLog] | None = None
    selected_ssh_keys: set[int] = field(default_factory=set)

    server_loading_status: LoadState = LoadState.IDLE
    logs_loading_status: LoadState = LoadState.IDLE

    current_tab_index: int = 0

    def clear_selected_ssh_keys(self) -> None:
        self.selected_ssh_keys.clear()

    def add_selected_ssh_key(self, key_id: int) -> None:
        self.selected_ssh_keys.add(key_id)

    def discard_selected_ssh_keys(self, key_id: int) -> None:
        self.selected_ssh_keys.discard(key_id)

    def set_ssh_keys_list(self, ssh_keys_list: list[GetSSHKey]) -> None:
        self.ssh_keys_list = ssh_keys_list

    def set_server_loading_status(self, status: LoadState) -> None:
        self.server_loading_status = status

    def set_current_tab_index(self, index: int) -> None:
        self.current_tab_index = index

    def set_server(self, server: GetServer | None) -> None:
        self.server = server

    def set_logs_loading_status(self, status: LoadState) -> None:
        self.logs_loading_status = status

    def set_server_logs_list(self, logs_list: list[GetServerLog]) -> None:
        self.server_logs_list = logs_list
