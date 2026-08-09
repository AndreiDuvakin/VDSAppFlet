from urllib.parse import urljoin

from dataclass_rest.http.aiohttp import AiohttpMethod
from dataclass_rest.http_request import HttpRequest


class CustomHeadersAiohttpMethod(AiohttpMethod):
    async def _pre_process_request(self, request: HttpRequest) -> HttpRequest:
        request.headers["X-Token"] = self.client.token

        if not request.url.startswith('https://'):
            request.url = urljoin(self.client.base_url, request.url)

        return request
