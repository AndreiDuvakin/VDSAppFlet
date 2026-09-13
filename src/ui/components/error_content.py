from typing import Any, Callable, Coroutine

import flet as ft


@ft.component
def error_content(
    title: str,
    message: str,
    on_repeat: Callable[[], Coroutine[Any, Any, None]],
):
    return ft.Container(
        ft.Column(
            [
                ft.Icon(
                    ft.Icons.CLOUD_OFF_SHARP,
                    size=64,
                ),
                ft.Text(
                    title,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    message,
                    size=20,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Button(
                    "Повторить",
                    on_click=on_repeat,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
    )
