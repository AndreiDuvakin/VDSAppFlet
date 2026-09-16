import logging

import flet as ft

from src.core.contexts import AppContext

logger = logging.getLogger(__name__)


@ft.component
def protected_route():
    logger.info("Initializing protected route")

    app_state = ft.use_context(AppContext)

    if not app_state.is_authenticated:
        logger.warning("Authentication failed, return to auth page")
        ft.context.page.navigate("/auth")
        return ft.ProgressRing()

    logger.info("Authentication successful")

    return ft.use_route_outlet()
