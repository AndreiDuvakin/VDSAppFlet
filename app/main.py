import flet as ft

from api.servers_client import ServersClient
from app.api.account_client import AccountClient
from app.services.account_service import AccountService
from app.ui.views.account_view import AccountView
from services.servers_service import ServersService
from state.app_state import AppState
from ui.views.main_view import MainView

@ft.component
def AppRoot(page: ft.Page):
    token = "c0568931e74d193ce4d01d981fbfe2cfe92d0b860725d9ea6cc04b135faa6ae4"

    account_client = AccountClient(token)
    servers_client = ServersClient(token)

    state, set_state = ft.use_state(AppState())

    account_service = AccountService(
        client=account_client,
        set_state=set_state,
        page=page,
    )
    servers_service = ServersService(servers_client, state.servers, page)

    return AccountView(
        state=state,
        service=account_service,
        page=page,
    )


def main(page: ft.Page):
    page.title = "Vscale — Тест (dict state)"
    page.render(lambda: AppRoot(page))


ft.app(target=main)