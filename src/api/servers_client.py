from typing import List

from src.api.base import BaseVscaleClient


class ServersClient(BaseVscaleClient):
    async def list(self) -> list[dict]:
        return await self._get("/scalets")

    async def get(self, ctid: int) -> dict:
        return await self._get(f"/scalets/{ctid}")

    async def restart(self, ctid: int) -> dict:
        return await self._patch(f"/scalets/{ctid}/restart")

    async def start(self, ctid: int) -> dict:
        return await self._patch(f"/scalets/{ctid}/start")

    async def stop(self, ctid: int) -> dict:
        return await self._patch(f"/scalets/{ctid}/stop")

    async def add_ssh_key(self, ctid: int, ssh_key_ids: List[int]) -> dict:
        return await self._patch(f"/scalets/{ctid}", data={"keys": ssh_key_ids})
