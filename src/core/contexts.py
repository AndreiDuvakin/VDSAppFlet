import flet as ft

from api.base import ApiClient
from state.auth_state import AuthState

AuthContext: ft.ContextProvider[AuthState | None] = ft.create_context(None)
ApiClientContext: ft.ContextProvider[ApiClient | None] = ft.create_context(None)
