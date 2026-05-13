from dataclasses import dataclass, field

import flet as ft

from domain.ssh_key import SSHKey


@ft.observable
@dataclass
class SSHKeysState:
    items: list[SSHKey] = field(default_factory=list)
    loading: bool = False
    error: str | None = None
