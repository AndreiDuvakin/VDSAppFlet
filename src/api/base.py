import logging

from api.account_client import AccountClient
from services.account_service import AccountService

logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = 'https://api.vscale.io/v1/'

    def __init__(self):
        logger.info('Initializing ApiClient')

        self.token = None
        self.it_is_ready = False

        self.account_client = None
        self.account_service = None

    def init_clients(self):
        logger.info('Creating api clients and services')

        self.it_is_ready = False

        if not isinstance(self.token, str):
            logger.warning('Fail initializing: Token must be a string')
            self.delete_clients_and_services()
            raise TypeError('Token must be a string')

        logger.info('Initializing AccountService and AccountClient')
        self.account_client = AccountClient(self.token, self.BASE_URL)
        self.account_service = AccountService(self.account_client)

        self.it_is_ready = True

    async def __aenter__(self):
        if not self.it_is_ready:
            raise TypeError('Clients are not ready')

        await self.account_client.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.account_client.__aexit__(exc_type, exc_val, exc_tb)

    def delete_clients_and_services(self):
        logger.info('Deleting clients and services')

        self.account_client = None
        self.account_service = None

    def set_token(self, token: str):
        logger.info('Setting token')

        self.token = token
        self.init_clients()
