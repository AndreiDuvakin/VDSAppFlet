import flet as ft


@ft.component
def empty_content(
    icon,
    title,
    text,
):
    return ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(icon, size=64, color=ft.Colors.GREY_400),
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            text,
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                expand=True,
                alignment=ft.Alignment.CENTER,
            ),
        ],
        expand=True,
    )
