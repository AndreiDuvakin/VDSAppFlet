import flet as ft

from routing.private_router import protected_route
from ui.pages.login_page import login_page


def app_router():
    return ft.Router(
        [
            ft.Route(
                path="/auth",
                component=login_page,
            ),
            ft.Route(
                component=protected_route,
            )
        ]
    )
