from dataclass_rest import get, put
from dataclass_rest.http.aiohttp import AiohttpClient

from api.custom_headers_aiohttp_method import CustomHeadersAiohttpMethod
from models.notification import GetNotificationSettings, PostNotificationSettings


class NotificationClient(AiohttpClient):
    method_class = CustomHeadersAiohttpMethod

    def __init__(self, token, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token

    @get('billing/notify')
    async def get_notification_settings(self) -> GetNotificationSettings:
        pass

    @put('billing/notify', send_json=False)
    async def post_notification_settings(self, body: PostNotificationSettings) -> GetNotificationSettings:
        pass
