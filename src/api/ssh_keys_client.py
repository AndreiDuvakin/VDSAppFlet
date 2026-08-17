from typing import List

from dataclass_rest import delete, get, post

from src.api.abstract_client import AbstractClient
from src.models.ssh_key import GetSSHKey, PostSSHKey


class SSHKeysClient(AbstractClient):
    @get("sshkeys")
    async def get_ssh_keys(self) -> List[GetSSHKey]:
        pass

    @post("sshkeys")
    async def create_ssh_key(self, body: PostSSHKey) -> GetSSHKey:
        pass

    @delete("sshkeys/{key_id}")
    async def delete_ssh_key_by_id(self, key_id: int) -> None:
        pass
