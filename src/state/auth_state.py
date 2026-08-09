from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class AuthState:
    is_authenticated: bool = False
    username: str = ""
    token: str = ""

    def login(self, token, username):
        self.token = token
        self.username = username
        self.is_authenticated = True

    def logout(self):
        self.token = ""
        self.username = ""
        self.is_authenticated = False
