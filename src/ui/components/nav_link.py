import flet as ft


@ft.component
def nav_link(icon, path):
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Icon(
            icon=icon,
            fill=1 if active else 0,
            color=ft.Colors.PRIMARY if active else ft.Colors.ON_SURFACE,
        ),
        bgcolor=ft.Colors.PRIMARY_CONTAINER if active else None,
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        border_radius=8,
        on_click=lambda: ft.context.page.navigate(path),
    )
