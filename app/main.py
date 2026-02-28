import os

import flet as ft
from dotenv import load_dotenv

from app.api.servers_client import ServersClient
from app.api.account_client import AccountClient
from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.state.app_state import AppState
from app.ui.views.main_view import MainView


@ft.component
def AppRoot(page: ft.Page):
    token = os.environ.get('TOKEN')

    account_client = AccountClient(token)
    servers_client = ServersClient(token)

    state, set_state = ft.use_state(AppState())

    account_service = AccountService(
        client=account_client,
        set_state=set_state,
    )
    servers_service = ServersService(servers_client, state.servers, page)

    return MainView(
        state=state,
        account_service=account_service,
        servers_service=servers_service,
        page=page,
    )


def main(page: ft.Page):
    load_dotenv()

    page.title = "Vscale — Тест (dict state)"
    page.render(lambda: AppRoot(page))


ft.app(target=main)