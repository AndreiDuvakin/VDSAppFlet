from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class AccountState:
    info: dict | None = None
    loading: bool = False
    error: str | None = None
