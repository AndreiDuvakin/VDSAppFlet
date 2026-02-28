import flet as ft

from app.services.account_service import AccountService
from app.state.app_state import AppState


@ft.component
def AccountView(state: AppState, service: AccountService, page: ft.Page) -> ft.Control:
    def start_loading():
        if state.account.info is None and not state.account.loading:
            page.run_task(service.load_account, state)

    ft.use_effect(start_loading, [state.account.loading, bool(state.account.info)])

    if state.account.loading:
        return ft.ProgressRing(width=50, height=50)

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