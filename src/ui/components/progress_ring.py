import flet as ft


def progress_ring() -> ft.Control:
    return ft.Container(
            ft.ProgressRing(),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )