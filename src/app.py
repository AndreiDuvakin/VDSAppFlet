import asyncio
import logging

import flet as ft

from src.api.base import ApiClient
from src.controllers.app_controller import AppController
from src.core.contexts import ApiClientContext, AppContext
from src.routing.router import app_router
from src.state.app_state import AppState
from src.state.load_state import LoadState
from src.ui.components.error_content import error_content
from src.ui.components.show_message_banner import show_message_banner

logger = logging.getLogger(__name__)


@ft.component
def app():
    logger.info("Creating states for contexts")
    api_client, _ = ft.use_state(ApiClient)
    app_state, _ = ft.use_state(AppState)
    page = ft.context.page

    app_controller = AppController(
        api_client.price_service,
        api_client.tags_service,
        app_state,
        lambda message: show_message_banner(message, page),
    )

    if (
        app_state.price is None
        and app_state.price_loading_status.value == LoadState.IDLE.value
        and app_state.token
    ):
        asyncio.create_task(app_controller.get_price())

    if (
        app_state.tags is None
        and app_state.tags_loading_status.value == LoadState.IDLE.value
        and app_state.token
    ):
        asyncio.create_task(app_controller.get_tags())

    if app_state.tags_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить теги серверов",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            app_controller.repeat_loading_tags,
        )

    if app_state.price_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить цены",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            app_controller.repeat_loading_price,
        )

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
