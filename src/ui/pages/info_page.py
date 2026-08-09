import flet as ft


@ft.component
def info_page():
    return ft.Column(
        [
            ft.Text("info page")
        ],
        expand=True,
    )
