from app.api.base import BaseVscaleClient


class SSHKeysClient(BaseVscaleClient):
    async def list(self) -> list[dict]:
        return await self._get("/sshkeys")

    async def delete(self, key_id: int) -> dict:
        return await self._delete(f"/sshkeys/{key_id}")

    async def create(self, name: str, key: str) -> dict:
        data = {
            "name": name,
            "key": key,
        }
        return await self._post("/sshkeys", data)
