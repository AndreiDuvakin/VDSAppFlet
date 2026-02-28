import flet as ft

from app.services.account_service import AccountService


@ft.component
def AccountView(state: dict, service: AccountService, page: ft.Page) -> ft.Control:
    acc = state["account"]

    def start_loading():
        if acc["info"] is None and not acc["loading"]:
            page.run_task(service.load_account)

    ft.use_effect(start_loading, [])

    if acc["loading"]:
        return ft.ProgressRing(width=50, height=50)

    if acc["error"]:
        return ft.Text(f"Ошибка: {acc['error']}", color="red")

    if not acc["info"]:
        return ft.Text("Аккаунт не загружен")

    info = acc["info"]
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