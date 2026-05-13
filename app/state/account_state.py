from dataclasses import dataclass

import flet as ft

from app.domain.account import Account


@ft.observable
@dataclass
class AccountState:
    info: Account | None = None
    loading: bool = False
    error: str | None = None
