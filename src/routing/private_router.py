import flet as ft

from core.contexts import AuthContext


@ft.component
def protected_route():
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()

    if not auth.is_authenticated:
        ft.context.page.navigate("/auth")
        return ft.ProgressRing()

    return outlet