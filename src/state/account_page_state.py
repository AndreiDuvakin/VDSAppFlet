import flet as ft

from dataclasses import dataclass


@dataclass
@ft.observable
class AccountPageState:
    is_loading: bool = False

    current_tab_index: int = 0

    def set_is_loading(self, is_loading: bool):
        self.is_loading = is_loading

    def set_current_tab_index(self, current_tab_index: int):
        self.current_tab_index = current_tab_index
