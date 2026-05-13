from dataclasses import replace
from typing import Any

from app.api.servers_client import ServersClient
from app.state.app_state import AppState
from app.domain.server import Server

class ServersService:
    def __init__(self, client: ServersClient, set_state):
        self.client = client
        self.set_state = set_state

    async def _update(self, state: AppState, **servers_changes: Any) -> AppState:
        new_servers = replace(state.servers, **servers_changes)
        new_state = replace(state, servers=new_servers)
        await self.set_state(new_state)
        return new_state

    async def load_servers(self, state: AppState) -> None:
        await self._update(state, loading=True, error=None)
        try:
            raw_servers = await self.client.list()
            servers = [Server.from_dict(item) for item in raw_servers]
            await self._update(state, items=servers, loading=False, error=None)
        except IOError as e:
            await self._update(state, items=[], loading=False, error=str(e))