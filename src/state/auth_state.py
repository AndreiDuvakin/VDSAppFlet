import logging
from dataclasses import dataclass, field

import flet as ft

from models.account import GetAccount
from state.account_page_state import AccountPageState

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
    is_authenticated: bool = False
    account: GetAccount | None = None
    token: str = ""

    is_login_loading: bool = False

    account_page_state: AccountPageState = field(
        default_factory=AccountPageState
    )

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
