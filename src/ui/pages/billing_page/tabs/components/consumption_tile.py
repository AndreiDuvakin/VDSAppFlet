import flet as ft

from ui.pages.billing_page.common import format_money, get_resource_name
from models.billing import BillingUsage


@ft.component
def create_consumption_tile(
        usage: BillingUsage,
) -> ft.Control:
    return ft.Card(
        content=ft.ListTile(
            leading=ft.Icon(
                ft.Icons.DNS_OUTLINED,
                color=ft.Colors.BLUE_400,
            ),
            title=ft.Text(
                get_resource_name(usage),
                weight=ft.FontWeight.W_500,
            ),
            subtitle=ft.Text(
                f'Количество: {usage.count}'
            ),
            trailing=ft.Text(
                format_money(usage.summ),
                color=ft.Colors.RED_600,
                weight=ft.FontWeight.BOLD,
            ),
        ),
    )
