import asyncio
import logging

import flet as ft

from api.base import ApiClient
from core.contexts import AppContext, ApiClientContext
from routing.router import app_router
from state.app_state import AppState
from ui.components.show_message_banner import show_message_banner

logger = logging.getLogger(__name__)

# TODO: mypy, flake8, black, poetry

@ft.component
def app():
    logger.info("Creating states for contexts")
    api_client, _ = ft.use_state(ApiClient)
    app_state, _ = ft.use_state(AppState)
    page = ft.context.page

    async def get_price():
        try:
            logger.info(f"Getting price")
            app_state.set_is_price_loading(True)

            price = await api_client.price_service.get_price()

            app_state.set_price(price)

        except Exception as e:
            logger.error(f'Error getting price: {e}')
            show_message_banner(
                "Ошибка получения цен.",
                page,
            )

        finally:
            app_state.set_is_price_loading(False)

    async def get_tags():
        try:
            logger.info(f"Getting tags")
            app_state.set_is_tags_loading(True)

            tags = await api_client.tags_service.get_tags()

            app_state.set_tags(tags)

        except Exception as e:
            logger.error(f'Error getting tags: {e}')
            show_message_banner(
                "Ошибка получения тегов серверов.",
                page,
            )

        finally:
            app_state.set_is_tags_loading(False)

    if app_state.price is None and not app_state.is_price_loading and app_state.token:
        asyncio.create_task(get_price())

    if app_state.tags is None and not app_state.is_tags_loading and app_state.token:
        asyncio.create_task(get_tags())

    logger.info("Returning app_router with contexts")

    return ft.SafeArea(
        content=ApiClientContext(
            api_client,
            lambda: AppContext(
                app_state,
                app_router,
            ),
        ),
        expand=True,
    )
