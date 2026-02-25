from app.api.base import BaseVscaleClient

class AccountClient(BaseVscaleClient):
    async def get(self) -> dict:
        data = await self._get("/account")
        return data.get("info", data)