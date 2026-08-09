import logging

import flet as ft

from routing.private_router import protected_route
from ui.layouts.app_layout import app_layout
from ui.pages.account_page.account_page import account_page
from ui.pages.info_page import info_page
from ui.pages.login_page import login_page
from ui.pages.servers_page import servers_page

logger = logging.getLogger(__name__)


@ft.component
def app_router():
    logger.info("Returning main app router")

    main_router = ft.Router(
        [
            ft.Route(
                path="/auth",
                component=login_page,
            ),
            ft.Route(
                component=protected_route,
                children=[
                    ft.Route(
                        component=app_layout,
                        children=[
                            ft.Route(
                                path="/servers",
                                component=servers_page,
                            ),
                            ft.Route(
                                path="/account",
                                component=account_page,
                            ),
                            ft.Route(
                                path="/info",
                                component=info_page,
                            )
                        ]
                    )
                ],
            )
        ]
    )

    return main_router
