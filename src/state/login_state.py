from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class LoginState:
    info: dict | None = None
    loading: bool = False
    error: str | None = None
