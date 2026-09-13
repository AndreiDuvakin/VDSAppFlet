import asyncio

import flet as ft


def show_message_banner(text, page: ft.Page, is_error=True, timer_sec: int = 3):
    async def autoclose_banner():
        await asyncio.sleep(timer_sec)
        pop_dialog()

    def pop_dialog():
        page.pop_dialog()

    page.show_dialog(
        ft.Banner(
            leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLACK),
            content=ft.Text(text, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.AMBER_100 if is_error else ft.Colors.GREEN_300,
            actions=[ft.TextButton()],
        )
    )

    if timer_sec:
        asyncio.create_task(autoclose_banner())
