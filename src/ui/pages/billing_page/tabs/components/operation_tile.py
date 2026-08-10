import flet as ft

from core.common import format_operation_price
from models.billing import BillingOperation


@ft.component
def create_operation_tile(
        operation: BillingOperation,
) -> ft.Control:
    is_success = operation.state == 1

    return ft.Container(
        content=ft.ListTile(
            leading=ft.Icon(
                ft.Icons.ARROW_UPWARD_ROUNDED,
                color=ft.Colors.GREEN_300,
            ),
            title=ft.Text(
                operation.desc or 'Операция',
                weight=ft.FontWeight.W_500,
            ),
            subtitle=ft.Text(
                operation.created.strftime('%d.%m.%Y, %H:%M')
            ),
            trailing=ft.Column(
                [
                    ft.Text(
                        format_operation_price(operation),
                        color=ft.Colors.GREEN_300,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        'Успешно' if is_success else 'Неизвестно',
                        size=12,
                        color=ft.Colors.GREEN_600
                        if is_success
                        else ft.Colors.GREY_500,
                    ),
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ),
        border=ft.Border(
            bottom=ft.BorderSide(
                1,
                ft.Colors.OUTLINE_VARIANT,
            ),
        ),
    )
