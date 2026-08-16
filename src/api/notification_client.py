from dataclass_rest import get, put

from api.abstract_client import AbstractClient
from models.notification import GetNotificationSettings, PostNotificationSettings


class NotificationClient(AbstractClient):
    @get("billing/notify")
    async def get_notification_settings(self) -> GetNotificationSettings:
        pass

    @put("billing/notify", send_json=False)
    async def post_notification_settings(
        self, body: PostNotificationSettings
    ) -> GetNotificationSettings:
        pass
