import logging

import flet as ft

from api.base import ApiClient
from core.contexts import AppContext, ApiClientContext
from routing.router import app_router
from state.auth_state import AppState

logger = logging.getLogger(__name__)


@ft.component
def app():
    logger.info("Creating states for contexts")
    api_client, _ = ft.use_state(ApiClient)
    app_state, _ = ft.use_state(AppState)

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
