import logging
from typing import List

from src.api.servers_client import ServersClient
from src.models.backup import GetBackup, PostBackup
from src.models.server import AddSSHKey, GetServer, GetServerLog, RenameServer

logger = logging.getLogger(__name__)


class ServersService:
    def __init__(self, servers_client: ServersClient) -> None:
        logger.info("Initializing Servers Service")

        self._client = servers_client

    async def get_servers(self) -> List[GetServer]:
        logger.info("Getting Servers")

        return await self._client.get_servers()

    async def stop_server(self, ctid: int) -> GetServer:
        logger.info("Stopping Server")

        return await self._client.stop_server(ctid)

    async def start_server(self, ctid: int) -> GetServer:
        logger.info("Starting Server")

        return await self._client.start_server(ctid)

    async def restart_server(self, ctid: int) -> GetServer:
        logger.info("Restarting Server")

        return await self._client.restart_server(ctid)

    async def get_server(self, ctid: int) -> GetServer:
        logger.info("Getting Server")

        return await self._client.get_server(ctid)

    async def rename_server(
        self,
        ctid: int,
        name: RenameServer,
    ) -> GetServer:
        logger.info("Renaming Server")

        return await self._client.rename_server(ctid, name)

    async def add_new_ssh_key_to_server(
        self,
        ctid: int,
        ssh_keys: AddSSHKey,
    ) -> GetServer:
        logger.info("Adding new SSH Keys to Server")

        return await self._client.add_new_ssh_key_to_server(ctid, ssh_keys)

    async def create_server_backup(
        self,
        ctid: int,
        body: PostBackup,
    ) -> GetBackup:
        logger.info("Creating Server Backup")

        return await self._client.create_server_backup(ctid, body)

    async def rebuild_server(self, ctid: int) -> GetServer:
        logger.info("Rebuilding Server")

        return await self._client.rebuild_server(ctid)

    async def get_logs_server(self, ctid: int) -> List[GetServerLog]:
        logger.info("Getting server logs")

        return await self._client.get_logs_server(ctid)

    async def delete_server(self, ctid: int) -> GetServer:
        logger.info("Deleting Server")

        return await self._client.delete_server(ctid)
