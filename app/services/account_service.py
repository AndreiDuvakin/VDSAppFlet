import flet as ft
from typing import Callable

from app.api.account_client import AccountClient
from app.state.app_state import AppState
from app.state.account_state import AccountState


class AccountService:
    def __init__(
        self,
        client: AccountClient,
        set_state: Callable[[AppState], None],
        page: ft.Page,
    ):
        self.client = client
        self.set_state = set_state
        self.page = page

    async def load_account(self, current_state: AppState) -> None:
        new_account = AccountState(
            info=None,
            loading=True,
            error=None,
        )
        new_state = AppState(
            current_tab=current_state.current_tab,
            account=new_account,
            servers=current_state.servers,
        )
        self.set_state(new_state)
        self.page.update()

        try:
            raw = await self.client.get()
            new_account = AccountState(
                info=raw,
                loading=False,
                error=None,
            )
        except Exception as e:
            new_account = AccountState(
                info=None,
                loading=False,
                error=str(e),
            )

        new_state = AppState(
            current_tab=current_state.current_tab,
            account=new_account,
            servers=current_state.servers,
        )
        self.set_state(new_state)
        self.page.update()