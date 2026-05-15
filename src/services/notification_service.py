from dataclasses import replace
from typing import Any

from src.api.notification_client import NotificationClient
from src.state.app_state import AppState
from src.domain.notification import NotificationSettings


class NotificationService:
    def __init__(self, client: NotificationClient, set_state):
        self.client = client
        self.set_state = set_state

    async def _update(self, state: AppState, **changes: Any) -> AppState:
        new_notification = replace(state.notification, **changes)
        new_state = replace(state, notification=new_notification)
        await self.set_state(new_state)
        return new_state

    async def load_settings(self, state: AppState) -> None:
        await self._update(state, loading=True, error=None)
        try:
            raw = await self.client.get_settings()
            settings = NotificationSettings.from_dict(raw)
            await self._update(state, settings=settings, loading=False, error=None)
        except Exception as e:
            await self._update(state, settings=None, loading=False, error=str(e))

    async def update_settings(self, state: AppState, notify_balance: int) -> None:
        await self._update(state, updating=True, error=None)
        try:
            raw = await self.client.update_settings(notify_balance)
            settings = NotificationSettings.from_dict(raw)
            await self._update(state, settings=settings, updating=False, error=None)
        except Exception as e:
            await self._update(state, updating=False, error=f"Ошибка сохранения: {str(e)}")
