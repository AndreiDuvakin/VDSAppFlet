from adaptix import ExtraSkip, Retort, name_mapping

from dataclass_rest.http.aiohttp import AiohttpClient

from src.api.custom_headers_aiohttp_method import CustomHeadersAiohttpMethod


class AbstractClient(AiohttpClient):
    method_class = CustomHeadersAiohttpMethod

    def __init__(self, token, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token

    def _init_response_body_factory(self) -> Retort:
        return Retort(
            recipe=[
                name_mapping(extra_in=ExtraSkip()),
            ],
        )
