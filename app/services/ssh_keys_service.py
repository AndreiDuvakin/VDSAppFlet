from dataclasses import replace
from typing import Any

from app.api.ssh_keys_client import SSHKeysClient
from app.state.app_state import AppState
from domain.ssh_key import SSHKey


class SSHKeysService:
    def __init__(self, client: SSHKeysClient, set_state):
        self.client = client
        self.set_state = set_state

    async def _update(self, state: AppState, **servers_changes: Any) -> AppState:
        new_ssh_keys = replace(state.ssh_keys, **servers_changes)
        new_state = replace(state, ssh_keys=new_ssh_keys)
        await self.set_state(new_state)
        return new_state

    async def load_ssh_keys(self, state: AppState) -> None:
        await self._update(state, loading=True, error=None)
        try:
            raw_ssh_keys = await self.client.list()
            ssh_keys = [SSHKey.from_dict(item) for item in raw_ssh_keys]
            await self._update(state, items=ssh_keys, loading=False, error=None)
        except IOError as e:
            await self._update(state, items=[], loading=False, error=str(e))

    async def delete_ssh_key(self, state: AppState, key_id: int) -> None:
        try:
            await self.client.delete(key_id)
            await self.load_ssh_keys(state)
        except Exception as e:
            await self._update(state, error=f"Ошибка удаления: {str(e)}")

    async def add_ssh_key(self, state: AppState, name: str, key: str) -> None:
        try:
            await self.client.create(name, key)
            await self.load_ssh_keys(state)
        except Exception as e:
            await self._update(state, error=f"Ошибка добавления: {str(e)}")