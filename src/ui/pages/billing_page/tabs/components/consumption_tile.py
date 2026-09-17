import logging

import flet as ft

from src.core.contexts import AppContext
from src.models.billing import BillingUsage
from src.ui.pages.billing_page.common import format_money, get_resource_name

logger = logging.getLogger(__name__)


@ft.component
def create_consumption_tile(
    usage: BillingUsage,
) -> ft.Control:
    app_state = ft.use_context(AppContext)

    try:
        server_id = int(usage.resource_id)
        server = app_state.get_server_by_id(server_id)

        if server is None:
            raise Exception(f"No server found with id {usage.resource_id}")

    except Exception as e:
        logger.warning(f"Error getting server: {e}")
        resource_name = get_resource_name(usage)

    else:
        resource_name = f"Сервер {server.name} {server.beautiful_name}"

    return ft.Card(
        content=ft.ListTile(
            leading=ft.Icon(
                ft.Icons.DNS_OUTLINED,
                color=ft.Colors.BLUE_400,
            ),
            title=ft.Text(
                resource_name,
                weight=ft.FontWeight.W_500,
            ),
            subtitle=ft.Text(f"Количество: {usage.count}"),
            trailing=ft.Text(
                format_money(usage.summ),
                color=ft.Colors.RED_600,
                weight=ft.FontWeight.BOLD,
            ),
        ),
    )
