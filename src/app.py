import flet as ft

from api.base import ApiClient
from core.contexts import AuthContext, ApiClientContext
from routing.router import app_router
from state.auth_state import AuthState


@ft.component
def app():
    api_client, _ = ft.use_state(ApiClient)
    auth, _ = ft.use_state(AuthState)

    return ft.SafeArea(
        content=ApiClientContext(
            api_client,
            AuthContext(
                auth,
                app_router,
            )
        )
    )
