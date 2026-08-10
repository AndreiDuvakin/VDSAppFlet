import flet as ft

from core.common import get_operation_word
from core.constants import MONTH_NAMES
from models.billing import BillingOperation
from ui.pages.billing_page.tabs.components.operation_tile import create_operation_tile


@ft.component
def billing_operations_view(
        grouped_operations: dict[
            int,
            dict[int, list[BillingOperation]],
        ],
):
    year_tiles = []

    for idx, (year, months) in enumerate(grouped_operations.items()):
        month_tiles = []

        for month_idx, (month, operations) in enumerate(months.items()):

            month_tiles.append(
                ft.ExpansionTile(
                    title=ft.Text(
                        MONTH_NAMES[month],
                        weight=ft.FontWeight.W_500,
                    ),
                    subtitle=ft.Text(
                        f'{len(operations)} '
                        f'{get_operation_word(len(operations))}'
                    ),
                    leading=ft.Icon(
                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                    ),
                    controls=[
                        ft.Column(
                            [
                                create_operation_tile(operation)
                                for operation in operations
                            ],
                            spacing=0,
                        ),
                    ],
                    expanded=not idx and not month_idx,
                )
            )

        year_tiles.append(
            ft.ExpansionTile(
                title=ft.Text(
                    str(year),
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                leading=ft.Icon(
                    ft.Icons.CALENDAR_TODAY_OUTLINED,
                ),
                expanded=not idx,
                controls=month_tiles,
            )
        )

    return ft.ListView(
        controls=year_tiles,
        spacing=8,
        expand=True,
        padding=ft.Padding.only(
            left=10,
            right=10,
            top=10,
            bottom=10,
        ),
    )
