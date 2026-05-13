from typing import Callable

import flet as ft

from api.account_client import AccountClient
from app.services.account_service import AccountService
from app.state.app_state import AppState


def AccountView(
        state: AppState,
        page: ft.Page,
        set_state: Callable
) -> ft.Control:
    page.title = 'Данные аккаунта'

    client = AccountClient(state.token)
    service = AccountService(client, set_state)

    if state.account.info is None and not state.account.loading and not state.account.error:
        page.run_task(service.load_account, state)

    if state.account.loading:
        return ft.Column(
            [ft.ProgressRing()],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    if state.account.error:
        return ft.Text(f"Ошибка: {state.account.error}", color="red")
    if not state.account.info:
        return ft.Text("Аккаунт не загружен")

    info = state.account.info
    return ft.Column(
        [
            ft.Text("✅ Аккаунт загружен", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Имя: {info.get('name')} {info.get('surname')}", size=18),
            ft.Text(f"Email: {info.get('email')}"),
            ft.Text(f"Статус: {'Активен' if info.get('state') == '1' else 'Неактивен'}"),
            ft.Text(f"Дата активации: {info.get('actdate')}"),
        ],
        spacing=15,
    )
