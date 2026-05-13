from dataclasses import dataclass, field

import flet as ft

from app.state.account_state import AccountState
from app.state.servers_state import ServersState
from state.login_state import LoginState
from state.ssh_keys_state import SSHKeysState


@ft.observable
@dataclass
class AppState:
    token: str | None = None
    temp_token: str = ""
    account: AccountState = field(default_factory=AccountState)
    servers: ServersState = field(default_factory=ServersState)
    login: LoginState = field(default_factory=LoginState)
    ssh_keys: SSHKeysState = field(default_factory=SSHKeysState)
