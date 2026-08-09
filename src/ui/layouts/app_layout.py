import flet as ft

from ui.components.nav_bar import nav_bar


@ft.component
def app_layout():
    outlet = ft.use_route_outlet()

    return ft.Column(
        [
            outlet,
            nav_bar(),
        ],
        expand=True,
    )
