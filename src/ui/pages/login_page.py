from typing import Callable

import flet as ft

from src.api.account_client import AccountClient
from src.services.login_service import LoginService
from src.state.app_state import AppState
from src.ui.components.progress_ring import progress_ring
from src.ui.components.show_simple_dialog import show_simple_dialog


async def LoginPage(
        page: ft.Page,
        state: AppState,
        set_state: Callable,
        set_token: Callable,
) -> ft.Control:
    page.title = 'Вход'

    def handle_token_field_change(e):
        setattr(state, 'temp_token', e.control.value.strip())

    token_field = ft.TextField(
        label='Введите токен',
        on_change=handle_token_field_change,
        password=True,
        can_reveal_password=True,
    )

    async def check_token():
        token_value = state.temp_token
        if not token_value:
            show_simple_dialog('Внимание', ft.Text('Заполните поле ввода токена'), page)
            return
        account_client = AccountClient(token_value)
        login_service = LoginService(account_client, set_state)
        page.run_task(login_service.load_account, state)

    if state.login.loading:
        return progress_ring()

    if state.login.error:
        show_simple_dialog('Ошибка входа', ft.Text('Неправильный токен'), page)
        state.login.error = None

    if state.login.info:
        if state.temp_token:
            await set_token(state.temp_token)
            state.temp_token = ""

    return ft.Column(
        [
            ft.Text(
                'Для продолжения введите токен аутентификации из личного кабинета VDS Selectel',
                text_align=ft.TextAlign.CENTER,
            ),
            token_field,
            ft.OutlinedButton(
                'Войти',
                on_click=check_token,
            )
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )
