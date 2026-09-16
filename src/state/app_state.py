from dataclasses import dataclass, field
import logging
from typing import List

import flet as ft
import flet_secure_storage as fss

from src.core.storage_factory import create_secure_storage
from src.models.account import GetAccount
from src.models.price import GetPrice
from src.models.server import GetServer
from src.models.tag import GetTag
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
    secure_storage: fss.SecureStorage | None = field(
        default_factory=create_secure_storage
    )
    is_authenticated: bool = False
    account: GetAccount | None = None

    servers: List[GetServer] | None = None
    tags: List[GetTag] | None = None

    price: GetPrice | None = None
    token: str = ""

    token_secure_check_status: LoadState = LoadState.IDLE
    login_loading_status: LoadState = LoadState.IDLE
    price_loading_status: LoadState = LoadState.IDLE
    tags_loading_status: LoadState = LoadState.IDLE

    async def get_token(self) -> str | None:
        return await self.secure_storage.get("token")

    async def set_token(self, token) -> None:
        await self.secure_storage.set("token", token)

    async def clear_storage(self) -> None:
        print(3333333333333333333333333)
        await self.secure_storage.clear()
        print(44444444444444444444444444)

    def set_token_secure_check_status(self, status: LoadState):
        self.token_secure_check_status = status

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

    def login(self, token, account):
        logger.info("logining in app")

        self.token = token
        self.account = account
        self.is_authenticated = True

    async def logout(self):
        logger.info("logouting in app")

        self.is_authenticated = False
        self.token = ""
        self.account = None

        await self.clear_storage()
