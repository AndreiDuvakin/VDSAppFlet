from dataclasses import dataclass, field
import flet as ft

from app.state.account_state import AccountState
from app.state.servers_state import ServersState

@ft.observable
@dataclass
class AppState:
    current_screen: str = "account"
    account: AccountState = field(default_factory=AccountState)
    servers: ServersState = field(default_factory=ServersState)