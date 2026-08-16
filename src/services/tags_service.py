import logging
from typing import List

from api.tags_client import TagsClient
from models.tag import GetTag

logger = logging.getLogger(__name__)


class TagsService:
    def __init__(self, tags_client: TagsClient):
        logger.info('Initializing TagsService')

        self._client = tags_client

    async def get_tags(self) -> List[GetTag]:
        logger.info('Getting tags')

        return await self._client.get_tags()
