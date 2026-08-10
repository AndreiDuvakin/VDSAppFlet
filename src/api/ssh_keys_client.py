from typing import List

from dataclass_rest import get, post, delete
from dataclass_rest.http.aiohttp import AiohttpClient

from api.custom_headers_aiohttp_method import CustomHeadersAiohttpMethod
from models.ssh_key import GetSSHKey, PostSSHKey


class SSHKeysClient(AiohttpClient):
    method_class = CustomHeadersAiohttpMethod

    def __init__(self, token, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token

    @get('sshkeys')
    async def get_ssh_keys(self) -> List[GetSSHKey]:
        ...

    @post('sshkeys')
    async def create_ssh_key(self, body: PostSSHKey) -> GetSSHKey:
        ...

    @delete('sshkeys/{key_id}')
    async def delete_ssh_key_by_id(self, key_id: int) -> None:
        ...
