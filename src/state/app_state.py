from dataclasses import dataclass
import logging
from typing import List

import flet as ft

from src.models.account import GetAccount
from src.models.price import GetPrice
from src.models.server import GetServer
from src.models.tag import GetTag
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
    is_authenticated: bool = False
    account: GetAccount | None = None

    servers: List[GetServer] | None = None
    tags: List[GetTag] | None = None

    price: GetPrice | None = None
    token: str = ""

    login_loading_status: LoadState = LoadState.IDLE
    price_loading_status: LoadState = LoadState.IDLE
    tags_loading_status: LoadState = LoadState.IDLE

    is_login_loading: bool = False

    def set_login_loading_status(self, status: LoadState):
        self.login_loading_status = status

    def set_price_loading_status(self, status: LoadState):
        self.price_loading_status = status

    def set_tags_loading_status(self, status: LoadState):
        self.tags_loading_status = status

    def set_price(self, price: GetPrice):
        self.price = price

    def set_tags(self, tags: List[GetTag]):
        self.tags = tags

    def get_tags_by_server_ctid(self, ctid: int) -> List[GetTag]:
        if not self.tags:
            return []

        return [tag for tag in self.tags if ctid in tag.scalets]

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
