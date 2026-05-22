import flet as ft

from src.services.app_services import AppServices
from src.state.app_state import AppState
from src.ui.components.progress_ring import progress_ring
from src.ui.pages.servers_page.components.server_card import server_card


def servers_page(
        state: AppState,
        page: ft.Page,
        services: AppServices,
) -> ft.Control:
    page.title = 'Серверы'

    if not state.servers.items and not state.servers.loading and not state.servers.error:
        page.run_task(services.servers_service.load_servers, state)

    if not state.ssh_keys.items and not state.ssh_keys.loading:
        page.run_task(services.ssh_keys_service.load_ssh_keys, state)

    if state.servers.loading:
        return progress_ring()

    if state.servers.error:
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED_400),
                ft.Text(f"Ошибка: {state.servers.error}", size=16),
                ft.ElevatedButton("Повторить",
                                  on_click=lambda _: page.run_task(services.servers_service.load_servers, state))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    if not state.servers.items:
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DNS_OUTLINED, size=80, color=ft.Colors.GREY_400),
                ft.Text("У вас пока нет серверов", size=20, weight=ft.FontWeight.BOLD),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    cards = [
        server_card(page, server, services, state)
        for server in state.servers.items
    ]

    return ft.Column(
        [
            ft.Text("Ваши серверы", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Всего: {len(state.servers.items)}", color=ft.Colors.GREY_600),
            ft.Divider(),
            ft.ListView(
                controls=cards,
                expand=True,
                spacing=8,
            ),
        ],
        expand=True,
        spacing=15,
    )
