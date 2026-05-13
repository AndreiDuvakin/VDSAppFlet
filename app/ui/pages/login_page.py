from typing import Callable

import flet as ft

from app.api.account_client import AccountClient
from services.login_service import LoginService
from state.app_state import AppState


async def LoginPage(
        page: ft.Page,
        state: AppState,
        set_state: Callable,
        set_token: Callable,
) -> ft.Control:
    page.title = 'Вход'

    def show_simple_dialog(title: str, content: ft.Control):
        cupertino_actions = [
            ft.CupertinoDialogAction(
                destructive=True,
                content="Закрыть",
                on_click=handle_action_click,
            ),
        ]
        dialog = ft.CupertinoAlertDialog(
            title=title,
            content=content,
            actions=cupertino_actions,
        )
        page.show_dialog(dialog)

    def handle_action_click(e):
        page.pop_dialog()

    def handle_token_field_change(e):
        setattr(state, 'temp_token', e.control.value.strip())

    token_field = ft.TextField(
        label='Введите токен',
        on_change=handle_token_field_change,
    )

    async def check_token():
        token_value = state.temp_token
        if not token_value:
            show_simple_dialog('Внимание', ft.Text('Заполните поле ввода токена'))
            return
        account_client = AccountClient(token_value)
        login_service = LoginService(account_client, set_state)
        page.run_task(login_service.load_account, state)

    if state.login.loading:
        return ft.Column(
            [ft.ProgressRing()],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    if state.login.error:
        show_simple_dialog('Ошибка входа', ft.Text('Неправильный токен'))

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
