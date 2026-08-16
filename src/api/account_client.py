from dataclass_rest import get

from api.abstract_client import AbstractClient
from models.account import GetAccount


class AccountClient(AbstractClient):
    @get("account")
    async def get_account(self) -> GetAccount:
        pass
