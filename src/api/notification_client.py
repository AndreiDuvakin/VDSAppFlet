from src.api.base import BaseVscaleClient


class NotificationClient(BaseVscaleClient):
    async def get_settings(self) -> dict:
        return await self._get("/billing/notify")

    async def update_settings(self, notify_balance: int) -> dict:
        return await self._put(
            "/billing/notify",
            data={"notify_balance": notify_balance}
        )
