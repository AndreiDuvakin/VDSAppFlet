from dataclasses import dataclass
from typing import List

import flet as ft

from src.models.ssh_key import GetSSHKey


@dataclass
@ft.observable
class AccountPageState:
    is_loading_ssh_keys: bool = False
    is_loading_notifications: bool = False

    ssh_keys: List[GetSSHKey] | None = None
    notification_settings: int | None = None

    current_tab_index: int = 0

    def set_notification_balance(self, balance: int):
        self.notification_settings = balance

    def append_ssh_key(self, ssh_key: GetSSHKey) -> None:
        self.ssh_keys.append(ssh_key)

    def set_ssh_keys(self, ssh_keys: List[GetSSHKey]):
        self.ssh_keys = ssh_keys

    def set_is_loading_ssh_keys(self, is_loading: bool):
        self.is_loading_ssh_keys = is_loading

    def set_is_loading_notifications(self, is_loading: bool):
        self.is_loading_notifications = is_loading

    def set_current_tab_index(self, current_tab_index: int):
        self.current_tab_index = current_tab_index
