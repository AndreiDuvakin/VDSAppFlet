from dataclass_rest import get

from src.api.abstract_client import AbstractClient
from src.models.account import GetAccount


class AccountClient(AbstractClient):
    @get("account")
    async def get_account(self) -> GetAccount:
        pass
