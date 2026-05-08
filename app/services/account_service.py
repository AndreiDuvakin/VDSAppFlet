from dataclasses import replace
from typing import Any

from app.api.account_client import AccountClient
from app.state.app_state import AppState

class AccountService:
    def __init__(self, client: AccountClient, set_state):
        self.client = client
        self.set_state = set_state

    async def _update(self, state: AppState, **account_changes: Any) -> AppState:
        new_account = replace(state.account, **account_changes)
        new_state = replace(state, account=new_account)
        self.set_state(new_state)
        return new_state

    async def load_account(self, state: AppState) -> None:
        await self._update(state, loading=True, error=None)
        try:
            raw = await self.client.get()
            await self._update(state, info=raw, loading=False, error=None)
        except Exception as e:
            await self._update(state, info=None, loading=False, error=str(e))