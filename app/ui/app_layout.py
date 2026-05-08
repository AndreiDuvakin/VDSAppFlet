import flet as ft

from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.state.app_state import AppState
from app.ui.pages.account_page import AccountView
from app.ui.pages.servers_page import ServersView


@ft.component
def AppLayout(
        page: ft.Page,
        state: AppState,
        account_service: AccountService,
        servers_service: ServersService,
) -> ft.Control:
    # Определяем текущий экран по маршруту
    route = page.route.lstrip("/") or "account"

    # Отображаем соответствующий view
    if route == "account":
        content = AccountView(state=state, service=account_service, page=page)
    elif route == "servers":
        content = ServersView(state=state, service=servers_service)
    else:
        content = ft.Text("Страница не найдена", size=24, color="red")

    # Индекс для выделения пункта меню
    selected_index = 0 if route == "account" else 1

    return ft.Column(
        expand=True,
        controls=[
            ft.AppBar(title=ft.Text("Vscale Client")),
            ft.Container(content=content, expand=True),

        ]
    )