from typing import List

from dataclass_rest import get

from src.api.abstract_client import AbstractClient
from src.models.backup import GetBackup


class BackupsClient(AbstractClient):
    @get("backups")
    async def get_backups(self) -> List[GetBackup]:
        pass
