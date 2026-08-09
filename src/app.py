import logging

import flet as ft

from api.base import ApiClient
from core.contexts import AuthContext, ApiClientContext
from routing.router import app_router
from state.auth_state import AuthState

logger = logging.getLogger(__name__)


@ft.component
def app():
    logger.info("Creating states for contexts")
    api_client, _ = ft.use_state(ApiClient)
    auth_state, _ = ft.use_state(AuthState)

    logger.info("Returning app_router with contexts")

    return ft.SafeArea(
        content=ApiClientContext(
            api_client,
            lambda: AuthContext(
                auth_state,
                app_router,
            ),
        ),
    )
