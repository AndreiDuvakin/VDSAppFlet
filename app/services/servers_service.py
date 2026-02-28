from app.api.servers_client import ServersClient
from app.state.servers_state import ServersState
from app.domain.server import Server


class ServersService:
    def __init__(self, client: ServersClient, state: ServersState, page):
        self.client = client
        self.state = state

    def load(self) -> None:
        self.state.loading = True
        try:
            raw_servers = self.client.list()
            servers = [Server.from_dict(item) for item in raw_servers]
            self.state.items = servers
        except Exception as e:
            self.state.error = str(e)
        finally:
            self.state.loading = False
