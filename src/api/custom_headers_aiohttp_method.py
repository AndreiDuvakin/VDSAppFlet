from http import HTTPStatus
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientResponse

from dataclass_rest.http.aiohttp import AiohttpMethod
from dataclass_rest.http_request import HttpRequest


class CustomHeadersAiohttpMethod(AiohttpMethod):
    async def _pre_process_request(self, request: HttpRequest) -> HttpRequest:
        request.headers["X-Token"] = self.client.token

        if not request.url.startswith("https://"):
            request.url = urljoin(self.client.base_url, request.url)

        return request

    async def _response_body(
        self,
        response: ClientResponse,
    ) -> Any:
        if response.status == HTTPStatus.NO_CONTENT:
            return None

        return await super()._response_body(response)
