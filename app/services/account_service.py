import httpx

from app.api.account_client import AccountClient
from app.state.account_state import AccountState


class AccountService:
    def __init__(self, client: AccountClient, state: AccountState):
        self.client = client
        self.state = state

    def load_account(self) -> None:
        self.state.loading = True
        try:
            raw = self.client.get()
            self.state.info = raw
        except httpx.HTTPStatusError as e:
            self.state.error = f"API error {e.response.status_code}: {e.response.text}"
        except Exception as e:
            self.state.error = str(e)
        finally:
            self.state.loading = False
