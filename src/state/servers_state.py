import flet as ft

from dataclasses import dataclass, field

from src.domain.server import Server


@ft.observable
@dataclass
class ServersState:
    items: list[Server] = field(default_factory=list)
    loading: bool = False
    error: str | None = None
    selected_ctid: int | None = None