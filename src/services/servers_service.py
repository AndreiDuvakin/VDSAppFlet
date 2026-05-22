import time
from dataclasses import replace
from typing import Any, List

from src.api.servers_client import ServersClient
from src.state.app_state import AppState
from src.domain.server import Server


class ServersService:
    def __init__(self, client: ServersClient, set_state):
        self.client = client
        self.set_state = set_state
        self.last_refresh = time.time()

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
        except Exception as e:
            await self._update(state, items=[], loading=False, error=str(e))

    async def refresh_servers(self, state: AppState) -> None:
        if state.servers.loading:
            return

        await self._update(state, loading=False, error=None)
        try:
            raw_servers = await self.client.list()
            servers = [Server.from_dict(item) for item in raw_servers]
            await self._update(state, items=servers, loading=False, error=None)
        except Exception as e:
            await self._update(state, items=[], loading=False, error=str(e))

    async def start_server(self, state: AppState, ctid: int) -> None:
        new_updating_servers_ctids = state.servers.updating_servers_ctids
        new_updating_servers_ctids.append(ctid)
        await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        try:
            await self.client.start(ctid)
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        except Exception as e:
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=str(e))
        finally:
            await self.refresh_servers(state)

    async def stop_server(self, state: AppState, ctid: int) -> None:
        new_updating_servers_ctids = state.servers.updating_servers_ctids
        new_updating_servers_ctids.append(ctid)
        await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        try:
            await self.client.stop(ctid)
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        except Exception as e:
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=str(e))
        finally:
            await self.refresh_servers(state)

    async def restart_server(self, state: AppState, ctid: int) -> None:
        new_updating_servers_ctids = state.servers.updating_servers_ctids
        new_updating_servers_ctids.append(ctid)
        await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        try:
            await self.client.restart(ctid)
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        except Exception as e:
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=str(e))
        finally:
            await self.refresh_servers(state)

    async def add_ssh_key(self, state: AppState, ctid: int, ssh_key_ids: List[int]) -> None:
        new_updating_servers_ctids = state.servers.updating_servers_ctids
        new_updating_servers_ctids.append(ctid)
        await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        try:
            await self.client.add_ssh_key(ctid, ssh_key_ids)
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=None)
        except Exception as e:
            new_updating_servers_ctids.remove(ctid)
            await self._update(state, updating_servers_ctids=new_updating_servers_ctids, loading=False, error=str(e))
        finally:
            await self.refresh_servers(state)
