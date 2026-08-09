from api.account_client import AccountClient
from services.account_service import AccountService


class ApiClient:
    BASE_URL = 'https://api.vscale.io/v1'

    def __init__(self):
        self.token = None
        self._session_kwargs = None
        self.it_is_ready = False

        self.account_client = None
        self.account_service = None

    def init_clients(self):
        self.it_is_ready = False

        if not isinstance(self.token, str):
            self.delete_clients()
            raise TypeError('Token must be a string')

        headers = {"Authorization": f"Bearer {self.token}"}

        self._session_kwargs = {
            "base_url": self.BASE_URL,
            "headers": headers,
        }

        self.account_client = AccountClient(**self._session_kwargs)
        self.account_service = AccountService(self.account_client)

        self.it_is_ready = True

    async def __aenter__(self):
        if not self.it_is_ready:
            raise TypeError('Clients are not ready')

        await self.account_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.account_client.__aexit__(exc_type, exc_val, exc_tb)

    def delete_clients(self):
        self.account_client = None

    def set_token(self, token: str):
        self.token = token
        self.init_clients()
