from typing import List

from dataclass_rest import get, patch

from api.abstract_client import AbstractClient
from models.server import GetServer


class ServersClient(AbstractClient):
    @get('scalets')
    async def get_servers(self) -> List[GetServer]:
        pass

    @patch('scalets/{ctid}/stop')
    async def stop_server(self, ctid: int) -> GetServer:
        pass

    @patch('scalets/{ctid}/start')
    async def start_server(self, ctid: int) -> GetServer:
        pass

    @patch('scalets/{ctid}/restart')
    async def restart_server(self, ctid: int) -> GetServer:
        pass
