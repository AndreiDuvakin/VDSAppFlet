import logging

from api.account_client import AccountClient
from models.account import GetAccount

logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, account_client: AccountClient):
        logger.info("Initializing AccountService")

        self._client = account_client

    async def get_account(self) -> GetAccount:
        logger.info("Getting Account info")

        return await self._client.get_account()
