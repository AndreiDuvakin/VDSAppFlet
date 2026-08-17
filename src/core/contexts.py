import logging

import flet as ft

from src.api.base import ApiClient
from src.state.account_page_state import AccountPageState
from src.state.app_state import AppState
from src.state.billing_page_state import BillingPageState
from src.state.server_detail_page_state import ServerDetailPageState

logger = logging.getLogger(__name__)

logger.info("Initializing contexts")

AppContext: ft.ContextProvider[AppState | None] = ft.create_context(None)
ApiClientContext: ft.ContextProvider[ApiClient | None] = ft.create_context(None)
AccountPageContext: ft.ContextProvider[AccountPageState | None] = ft.create_context(
    None
)
BillingPageContext: ft.ContextProvider[BillingPageState | None] = ft.create_context(
    None
)
ServerDetailPageContext: ft.ContextProvider[ServerDetailPageState | None] = (
    ft.create_context(None)
)
