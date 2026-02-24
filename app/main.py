import flet as ft

from app.api.account_client import AccountClient
from app.api.servers_client import ServersClient
from app.services.account_service import AccountService
from app.services.servers_service import ServersService
from app.state.app_state import AppState
from app.ui.views.main_view import MainView


@ft.component
def AppRoot(page: ft.Page) -> list[ft.Control]:
    token = "c0568931e74d193ce4d01d981fbfe2cfe92d0b860725d9ea6cc04b135faa6ae4"

    account_client = AccountClient(token)
    servers_client = ServersClient(token)

    state, set_state = ft.use_state(AppState())

    account_service = AccountService(account_client, state.account)
    servers_service = ServersService(servers_client, state.servers)


    return MainView(
        state=state,
        account_service=account_service,
        servers_service=servers_service,
        page=page,
    )


def main(page: ft.Page):
    page.render(lambda: AppRoot(page))


ft.run(main)
