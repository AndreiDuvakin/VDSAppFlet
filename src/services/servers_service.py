import logging
from typing import List

from src.api.servers_client import ServersClient
from src.models.server import GetServer, GetServerLog, RenameServer

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

    async def rename_server(self, ctid: int, name: RenameServer) -> GetServer:
        logger.info("Renaming Server")

        return await self._client.rename_server(ctid, name)

    async def get_logs_server(self, ctid: int) -> List[GetServerLog]:
        logger.info("Getting server logs")

        return await self._client.get_logs_server(ctid)
