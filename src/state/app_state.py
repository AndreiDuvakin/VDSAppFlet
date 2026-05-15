from dataclasses import dataclass, field

import flet as ft

from src.state.account_state import AccountState
from src.state.servers_state import ServersState
from src.state.login_state import LoginState
from src.state.notification_state import NotificationState
from src.state.ssh_keys_state import SSHKeysState


@ft.observable
@dataclass
class AppState:
    token: str | None = None
    temp_token: str = ""

    account: AccountState = field(default_factory=AccountState)
    account_tab_index: int = 0

    servers: ServersState = field(default_factory=ServersState)
    login: LoginState = field(default_factory=LoginState)
    ssh_keys: SSHKeysState = field(default_factory=SSHKeysState)
    notification: NotificationState = field(default_factory=NotificationState)
