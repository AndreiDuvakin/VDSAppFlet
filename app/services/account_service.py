import flet as ft

from app.api.account_client import AccountClient


class AccountService:
    def __init__(self, client: AccountClient, state: dict, set_state):
        self.client = client
        self.state = state
        self.set_state = set_state

    async def load_account(self) -> None:
        new_state = {"account": {"info": None, "loading": True, "error": None}}
        self.set_state(new_state)

        try:
            raw = await self.client.get()

            new_state = {"account": {"info": raw, "loading": False, "error": None}}
        except Exception as e:
            new_state = {"account": {"info": None, "loading": False, "error": str(e)}}

        self.set_state(new_state)
