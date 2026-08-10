import logging

import flet as ft

from api.base import ApiClient
from state.account_page_state import AccountPageState
from state.app_state import AppState
from state.billing_page_state import BillingPageState

logger = logging.getLogger(__name__)

logger.info("Initializing contexts")

AppContext: ft.ContextProvider[AppState | None] = ft.create_context(None)
ApiClientContext: ft.ContextProvider[ApiClient | None] = ft.create_context(None)
AccountPageContext: ft.ContextProvider[AccountPageState | None] = ft.create_context(None)
BillingPageContext: ft.ContextProvider[BillingPageState | None] = ft.create_context(None)
