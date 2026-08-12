import flet as ft

from ui.pages.billing_page.common import format_money, get_resource_word
from core.constants import MONTH_NAMES
from models.billing import BillingUsage
from ui.pages.billing_page.tabs.components.consumption_tile import create_consumption_tile


@ft.component
def billing_consumption_view(
    billing_consumption: dict[
        int,
        dict[int, list[BillingUsage]],
    ],
) -> ft.Control:
    #TODO: сделать отображение названия серверов и тарифов

    year_tiles: list[ft.Control] = []

    for year, months in billing_consumption.items():
        month_tiles: list[ft.Control] = []

        for month, usages in months.items():
            month_total = sum(
                usage.summ
                for usage in usages
            )

            month_tiles.append(
                ft.ExpansionTile(
                    title=ft.Text(
                        MONTH_NAMES.get(
                            month,
                            str(month),
                        ),
                        weight=ft.FontWeight.W_500,
                    ),
                    subtitle=ft.Text(
                        (
                            f'{len(usages)} '
                            f'{get_resource_word(len(usages))} · '
                            f'{format_money(month_total)}'
                        ),
                    ),
                    leading=ft.Icon(
                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                    ),
                    controls=[
                        ft.Column(
                            [
                                create_consumption_tile(usage)
                                for usage in usages
                            ],
                            spacing=4,
                        ),
                    ],
                )
            )

        year_total = sum(
            usage.summ
            for months_items in months.values()
            for usage in months_items
        )

        year_tiles.append(
            ft.ExpansionTile(
                title=ft.Text(
                    str(year),
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                subtitle=ft.Text(
                    f'Всего за год: {format_money(year_total)}'
                ),
                leading=ft.Icon(
                    ft.Icons.CALENDAR_TODAY_OUTLINED,
                ),
                expanded=year == max(
                    billing_consumption,
                    default=year,
                ),
                controls=month_tiles,
            )
        )

    return ft.ListView(
        controls=year_tiles,
        spacing=8,
        padding=ft.Padding.only(
            left=10,
            right=10,
            top=10,
            bottom=10,
        ),
        expand=True,
    )