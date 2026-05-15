from dataclasses import replace
from typing import Any

from src.api.account_client import AccountClient
from src.state.app_state import AppState

class LoginService:
    def __init__(self, client: AccountClient, set_state):
        self.client = client
        self.set_state = set_state

    async def _update(self, state: AppState, **login_changes: Any) -> AppState:
        new_login = replace(state.login, **login_changes)
        new_state = replace(state, login=new_login)
        await self.set_state(new_state)
        return new_state

    async def load_account(self, state: AppState) -> None:
        await self._update(state, loading=True, error=None)
        try:
            raw = await self.client.get()
            await self._update(state, info=raw, loading=False, error=None)
        except Exception as e:
            await self._update(state, info=None, loading=False, error=str(e))