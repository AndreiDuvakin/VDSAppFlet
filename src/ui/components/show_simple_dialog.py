from typing import Callable

import flet as ft


def show_simple_dialog(
        title: str,
        content: ft.Control,
        page: ft.Page,
) -> None:
    def handle_action_click(e):
        page.pop_dialog()

    cupertino_actions = [
        ft.CupertinoDialogAction(
            destructive=True,
            content="Закрыть",
            on_click=handle_action_click,
        ),
    ]
    dialog = ft.CupertinoAlertDialog(
        title=title,
        content=content,
        actions=cupertino_actions,
    )
    page.show_dialog(dialog)
