from typing import List

from dataclass_rest import get, post

from src.api.abstract_client import AbstractClient
from src.models.tag import GetTag, PostTag


class TagsClient(AbstractClient):
    @get("scalets/tags/")
    async def get_tags(self) -> List[GetTag]:
        pass

    @post("scalets/tags")
    async def create_tag(self, body: PostTag) -> GetTag:
        pass
