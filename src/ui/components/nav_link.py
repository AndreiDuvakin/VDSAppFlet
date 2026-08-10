import flet as ft


@ft.component
def nav_link(icon, path, label):
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(
                        icon=icon,
                        color=ft.Colors.PRIMARY if active else ft.Colors.ON_SURFACE,
                    ),
                    bgcolor=ft.Colors.PRIMARY_CONTAINER if active else None,
                    border_radius=12,
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=20, vertical=5),
                ),
                ft.Text(label),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=lambda: ft.context.page.navigate(path),
    )
