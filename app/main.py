import flet as ft

from app.api.account_client import AccountClient
from app.services.account_service import AccountService
from app.ui.views.account_view import AccountView


@ft.component
def AppRoot(page: ft.Page) -> ft.Control:
    token = "цуацацупцупуц"
    account_client = AccountClient(token)

    initial_state = {
        "account": {
            "info": None,
            "loading": False,
            "error": None,
        }
    }

    state, set_state = ft.use_state(initial_state)

    account_service = AccountService(
        client=account_client,
        state=state,
        set_state=set_state,
    )

    return AccountView(
        state=state,
        service=account_service,
        page=page,
    )


def main(page: ft.Page):
    page.title = "Vscale — Тест (dict state)"
    page.render(lambda: AppRoot(page))


ft.app(target=main)