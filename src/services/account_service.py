from api.account_client import AccountClient
from models.account import GetAccount


class AccountService:
    def __init__(self, account_client: AccountClient):
        self._client = account_client

    async def get_account(self) -> GetAccount:
        return await self._client.get_account()
