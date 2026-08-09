import logging

import flet as ft

from api.base import ApiClient
from state.auth_state import AppState

logger = logging.getLogger(__name__)

logger.info("Initializing contexts")

AppContext: ft.ContextProvider[AppState | None] = ft.create_context(None)
ApiClientContext: ft.ContextProvider[ApiClient | None] = ft.create_context(None)
