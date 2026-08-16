import flet as ft


def show_message_banner(text, page: ft.Page, is_error=True):
    action_button_style = ft.ButtonStyle(color=ft.Colors.BLACK)

    def handle_action_click(e):
        page.pop_dialog()

    page.show_dialog(
        ft.Banner(
            leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLACK),
            content=ft.Text(text, color=ft.Colors.BLACK),
            actions=[
                ft.TextButton(
                    "Ок", on_click=handle_action_click, style=action_button_style
                )
            ],
            bgcolor=ft.Colors.AMBER_100 if is_error else ft.Colors.GREEN_300,
        )
    )
