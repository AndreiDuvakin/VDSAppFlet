import flet as ft


@ft.component
def progress_ring():
    return ft.Container(
        ft.ProgressRing(),
        expand=True,
        alignment=ft.Alignment.CENTER,
    )
