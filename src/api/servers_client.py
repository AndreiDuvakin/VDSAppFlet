from typing import List

from dataclass_rest import get, patch

from src.api.abstract_client import AbstractClient
from src.models.server import GetServer, GetServerLog, RenameServer


class ServersClient(AbstractClient):
    @get("scalets")
    async def get_servers(self) -> List[GetServer]:
        pass

    @get("scalets/{ctid}")
    async def get_server(self, ctid: int) -> GetServer:
        pass

    @patch("scalets/{ctid}/stop")
    async def stop_server(self, ctid: int) -> GetServer:
        pass

    @patch("scalets/{ctid}/start")
    async def start_server(self, ctid: int) -> GetServer:
        pass

    @patch("scalets/{ctid}/restart")
    async def restart_server(self, ctid: int) -> GetServer:
        pass

    @patch("scalets/{ctid}")
    async def rename_server(self, ctid: int, body: RenameServer) -> GetServer:
        pass

    @get("scalets/{ctid}/log")
    async def get_logs_server(self, ctid: int) -> List[GetServerLog]:
        pass
