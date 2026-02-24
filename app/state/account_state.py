import flet as ft

from dataclasses import dataclass


@ft.observable
@dataclass
class AccountState:
    info: dict | None = None
    loading: bool = False
    error: str | None = None
