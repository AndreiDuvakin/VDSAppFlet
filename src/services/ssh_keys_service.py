import logging

from api.ssh_keys_client import SSHKeysClient
from models.ssh_key import GetSSHKey, PostSSHKey

logger = logging.getLogger(__name__)


class SSHKeysService:
    def __init__(self, ssh_keys_client: SSHKeysClient):
        logger.info("Initializing SSHKeysService")

        self._client = ssh_keys_client

    async def get_ssh_keys(self) -> list[GetSSHKey]:
        logger.info("Getting ssh keys list info")

        return await self._client.get_ssh_keys()

    async def create_ssh_key(self, ssh_key: PostSSHKey) -> GetSSHKey:
        logger.info("Creating ssh key info")

        return await self._client.create_ssh_key(ssh_key)

    async def delete_ssh_key_by_id(self, key_id: int) -> None:
        logger.info("Deleting ssh key")

        return await self._client.delete_ssh_key_by_id(key_id)
