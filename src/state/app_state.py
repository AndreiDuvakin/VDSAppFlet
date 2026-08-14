import logging
from dataclasses import dataclass, field
from typing import List

import flet as ft

from models.account import GetAccount
from models.server import GetServer
from state.account_page_state import AccountPageState

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
    is_authenticated: bool = False
    account: GetAccount | None = None
    servers: List[GetServer] | None = None
    token: str = ""

    is_login_loading: bool = False

    account_page_state: AccountPageState = field(
        default_factory=AccountPageState
    )

    def get_server_by_id(self, ctid: int) -> GetServer | None:
        if self.servers is None:
            return None

        server = list(
            filter(
                lambda server: server.ctid == ctid,
                self.servers,
            )
        )

        if server:
            return server[0]

        return None

    def set_servers_list(self, servers_list: List[GetServer]):
        self.servers = servers_list

    def set_is_login_loading(self, is_login_loading: bool):
        self.is_login_loading = is_login_loading

    def login(self, token, account):
        logger.info("logining in app")

        self.token = token
        self.account = account
        self.is_authenticated = True

    def logout(self):
        logger.info("logouting in app")

        self.token = ""
        self.account = None
        self.is_authenticated = False
