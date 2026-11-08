import flet as ft


def show_message_banner(text, page: ft.Page, is_error=True):
    page.show_dialog(
        ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLACK),
                    ft.Text(text, color=ft.Colors.BLACK, no_wrap=False, expand=True),
                ]
            ),
            bgcolor=ft.Colors.AMBER_100 if is_error else ft.Colors.GREEN_300,
        )
    )
