from enum import Enum


class Screen(Enum):
    SERVERS = 'servers'
    ACCOUNT = 'account'
    SERVER_DETAILS = 'server_details'

    @staticmethod
    def server_details(ctid: int) -> str:
        return f"/server/{ctid}"

    @staticmethod
    def parse_server_route(route: str) -> int | None:
        if route.startswith("/server/"):
            try:
                return int(route.split("/")[-1])
            except ValueError:
                return None
        return None


SCREENS = list(Screen)
