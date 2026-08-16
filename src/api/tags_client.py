from typing import List

from dataclass_rest import get

from api.abstract_client import AbstractClient
from models.tag import GetTag


class TagsClient(AbstractClient):
    @get("scalets/tags/")
    async def get_tags(self) -> List[GetTag]:
        pass
