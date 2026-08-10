from dataclass_rest import get
from dataclass_rest.http.aiohttp import AiohttpClient

from api.custom_headers_aiohttp_method import CustomHeadersAiohttpMethod
from models.account import GetAccount


class AccountClient(AiohttpClient):
    method_class = CustomHeadersAiohttpMethod

    def __init__(self, token, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token

    @get('account')
    async def get_account(self) -> GetAccount:
        pass
