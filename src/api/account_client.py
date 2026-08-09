from dataclass_rest import get
from dataclass_rest.http.aiohttp import AiohttpClient

from models.account import GetAccount


class AccountClient(AiohttpClient):
    @get('/account')
    async def get_account(self) -> GetAccount:
        ...
