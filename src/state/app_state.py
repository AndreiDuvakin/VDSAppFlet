import logging
from dataclasses import dataclass
from typing import List

import flet as ft

from src.models.account import GetAccount
from src.models.price import GetPrice
from src.models.server import GetServer
from src.models.tag import GetTag

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

    is_login_loading: bool = False
    is_price_loading: bool = False
    is_tags_loading: bool = False

    def set_price(self, price: GetPrice):
        self.price = price

    def set_tags(self, tags: List[GetTag]):
        self.tags = tags

    def set_is_tags_loading(self, is_tags_loading: bool):
        self.is_tags_loading = is_tags_loading

    def set_is_price_loading(self, is_price_loading: bool):
        self.is_price_loading = is_price_loading

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
