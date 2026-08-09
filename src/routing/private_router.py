import logging

import flet as ft

from core.contexts import AppContext

logger = logging.getLogger(__name__)


@ft.component
def protected_route():
    logger.info("Initializing protected route")

    auth = ft.use_context(AppContext)
    outlet = ft.use_route_outlet()

    if not auth.is_authenticated:
        logger.warning("Authentication failed, return to auth page")
        ft.context.page.navigate("/auth")
        return ft.ProgressRing()

    logger.info("Authentication successful")

    return outlet
