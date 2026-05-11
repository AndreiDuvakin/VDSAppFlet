from app.api.base import BaseVscaleClient


class ServersClient(BaseVscaleClient):
    async def list(self) -> list[dict]:
        return await self._get("/scalets")

    async def get(self, ctid: int) -> list:
        return await self._get(f"/scalets/{ctid}")