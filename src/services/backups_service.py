import logging
from typing import List

from src.api.backups_client import BackupsClient
from src.models.backup import GetBackup

logger = logging.getLogger(__name__)


class BackupsService:
    def __init__(self, backups_client: BackupsClient):
        logger.info("Initializing BackupsService")

        self._client = backups_client

    async def get_backups(self) -> List[GetBackup]:
        logger.info("Getting backups")

        return await self._client.get_backups()
