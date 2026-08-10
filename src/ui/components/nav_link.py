import flet as ft


@ft.component
def nav_link(icon, path):
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Icon(
            icon=icon,
            color=ft.Colors.PRIMARY if active else ft.Colors.ON_SURFACE,
        ),
        bgcolor=ft.Colors.PRIMARY_CONTAINER if active else None,
        padding=ft.Padding.symmetric(horizontal=8, vertical=8),
        border_radius=8,
        on_click=lambda: ft.context.page.navigate(path),
        expand=True,
    )
