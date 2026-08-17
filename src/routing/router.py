import logging

import flet as ft

from src.routing.private_router import protected_route
from src.ui.layouts.app_layout import app_layout
from src.ui.pages.account_page.account_page import account_page
from src.ui.pages.billing_page.billing_page import billing_page
from src.ui.pages.info_page import info_page
from src.ui.pages.login_page import login_page
from src.ui.pages.server_detail_page.server_detail_page import server_detail_page
from src.ui.pages.servers_page.servers_page import servers_page

logger = logging.getLogger(__name__)


@ft.component
def app_router():
    logger.info("Returning main app router")

    return ft.Router(
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
                            ),
                            ft.Route(
                                path="/billing",
                                component=billing_page,
                            ),
                        ],
                    ),
                    ft.Route(
                        path="/server/:ctid",
                        component=server_detail_page,
                    ),
                ],
            ),
        ]
    )
