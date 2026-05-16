from typing import List

import flet as ft

from dataclasses import dataclass, field

from src.domain.server import Server


@ft.observable
@dataclass
class ServersState:
    items: list[Server] = field(default_factory=list)
    loading: bool = False
    error: str | None = None

    updating_servers_ctids: List[int] = field(default_factory=list)
