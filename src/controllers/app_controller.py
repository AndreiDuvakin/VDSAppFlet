import logging
from typing import Callable

from src.services.price_service import PriceService
from src.services.tags_service import TagsService
from src.state.app_state import AppState
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


class AppController:
    def __init__(
        self,
        price_service: PriceService,
        tags_service: TagsService,
        app_state: AppState,
        on_error: Callable[[str], None],
    ):
        self._price_service = price_service
        self._tags_service = tags_service
        self._app_state = app_state
        self._on_error = on_error

    async def get_price(self):
        try:
            logger.info("Getting price")
            self._app_state.set_price_loading_status(LoadState.LOADING)

            price = await self._price_service.get_price()

            self._app_state.set_price(price)

        except Exception as e:
            self._app_state.set_price_loading_status(LoadState.ERROR)
            logger.error(f"Error getting price: {e}")
            self._on_error("Ошибка получения цен.")

        else:
            self._app_state.set_price_loading_status(LoadState.SUCCESS)
            logger.info("Price loaded")

    async def get_tags(self):
        try:
            logger.info("Getting tags")
            self._app_state.set_tags_loading_status(LoadState.LOADING)

            tags = await self._tags_service.get_tags()

            self._app_state.set_tags(tags)

        except Exception as e:
            self._app_state.set_tags_loading_status(LoadState.ERROR)
            logger.error(f"Error getting tags: {e}")
            self._on_error("Ошибка получения тегов серверов.")

        else:
            logger.info("Tags loaded")
            self._app_state.set_tags_loading_status(LoadState.SUCCESS)

    async def repeat_loading_tags(self):
        logger.info("Repeat loading tags is started")
        await self.get_tags()

    async def repeat_loading_price(self):
        logger.info("Repeat loading price is started")
        await self.get_price()
