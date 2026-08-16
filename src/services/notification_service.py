import logging

from api.notification_client import NotificationClient
from models.notification import GetNotificationSettings, PostNotificationSettings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, notification_client: NotificationClient) -> None:
        logger.info("Initializing Notification Service")

        self._client = notification_client

    async def get_notification_settings(self) -> GetNotificationSettings:
        logger.info("Getting Notification Settings")

        return await self._client.get_notification_settings()

    async def post_notification_settings(
        self,
        notification_settings: PostNotificationSettings,
    ) -> GetNotificationSettings:
        logger.info("Posting Notification Settings")

        return await self._client.post_notification_settings(notification_settings)
