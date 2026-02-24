import flet as ft

from app.services.account_service import AccountService
from app.state.app_state import AppState


@ft.component
def AccountView(state: AppState, service: AccountService) -> ft.Control:
    info, set_info = ft.use_state(state.account.info)
    is_loading, set_is_loading = ft.use_state(state.account.loading)
    is_error, set_is_error = ft.use_state(state.account.error)

    def load_once():
        if state.account.info is None and not state.account.loading:
            service.load_account()

    ft.use_effect(load_once, [state.account])

    if is_loading:
        return ft.ProgressRing()

    if is_error:
        return ft.Text(f"Ошибка: {state.account.error}", color="red")

    if not info:
        return ft.Text("Аккаунт не загружен")


    return ft.Column([
        ft.Text(f"Имя: {info['name']} {info['surname']}", size=18),
        ft.Text(f"Email: {info['email']}"),
        ft.Text(f"Статус: {'Активен' if info['state'] == '1' else 'Неактивен'}"),
        ft.Text(f"Дата активации: {info['actdate']}"),
    ])
