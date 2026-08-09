import logging
from dataclasses import dataclass

import flet as ft

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AuthState:
    is_authenticated: bool = False
    username: str = ""
    token: str = ""

    is_loading: bool = False

    def set_loading(self, is_loading: bool):
        self.is_loading = is_loading

    def login(self, token, username):
        logger.info("logining in app")

        self.token = token
        self.username = username
        self.is_authenticated = True

    def logout(self):
        logger.info("logouting in app")

        self.token = ""
        self.username = ""
        self.is_authenticated = False
