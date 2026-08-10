from dataclasses import dataclass
from typing import List

import flet as ft

from models.ssh_key import GetSSHKey


@dataclass
@ft.observable
class AccountPageState:
    is_loading: bool = False

    ssh_keys: List[GetSSHKey] | None = None

    current_tab_index: int = 0

    def append_ssh_key(self, ssh_key: GetSSHKey) -> None:
        self.ssh_keys.append(ssh_key)

    def set_ssh_keys(self, ssh_keys: List[GetSSHKey]):
        self.ssh_keys = ssh_keys

    def set_is_loading(self, is_loading: bool):
        self.is_loading = is_loading

    def set_current_tab_index(self, current_tab_index: int):
        self.current_tab_index = current_tab_index
