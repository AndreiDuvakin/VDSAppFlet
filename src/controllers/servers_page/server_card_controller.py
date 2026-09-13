import logging
from typing import Any, Callable, Coroutine

from src.models.server import GetServer
from src.services.servers_service import ServersService
from src.state.app_state import AppState
from src.state.load_state import LoadState
from src.state.server_card_state import ServerCardState

logger = logging.getLogger(__name__)


class ServerCardController:
    def __init__(
        self,
        server_card_state: ServerCardState,
        servers_service: ServersService,
        app_state: AppState,
        server: GetServer,
        refresh_servers: Callable[[], Coroutine[Any, Any, None]],
        on_success: Callable[[str], None],
        on_error: Callable[[str], None],
    ):
        self._server_card_state = server_card_state
        self._servers_service = servers_service
        self._app_state = app_state
        self._server = server
        self._refresh_servers = refresh_servers
        self._on_success = on_success
        self._on_error = on_error

    async def stop_server(self, e):
        try:
            self._server_card_state.set_server_loading_status(LoadState.LOADING)

            await self._servers_service.stop_server(self._server.ctid)

        except Exception as e:  # noqa: F841
            self._server_card_state.set_server_loading_status(LoadState.ERROR)
            logger.error(f"Error stopping server: {e}")
            self._on_error(
                f"Ошибка остановки сервера {self._server.name}",
            )

        else:
            self._server_card_state.set_server_loading_status(LoadState.SUCCESS)
            logger.info(f"Server {self._server.ctid} stopped")
            self._on_success(f"Сервер {self._server.name} был остановлен")
            await self._refresh_servers()

    async def start_server(self, e):
        try:
            logger.info("Starting server")
            self._server_card_state.set_server_loading_status(LoadState.LOADING)

            await self._servers_service.start_server(self._server.ctid)

        except Exception as e:  # noqa: F841
            self._server_card_state.set_server_loading_status(LoadState.SUCCESS)
            logger.error(f"Error starting server: {e}")
            self._on_error(
                f"Ошибка запуска сервера {self._server.name}",
            )

        else:
            self._server_card_state.set_server_loading_status(LoadState.SUCCESS)
            logger.debug(f"Server {self._server.ctid} started")
            self._on_success(f"Сервер {self._server.name} был запущен")
            await self._refresh_servers()

    async def restart_server(self, e):
        try:
            logger.info("Restarting server")
            self._server_card_state.set_server_loading_status(LoadState.LOADING)

            await self._servers_service.restart_server(self._server.ctid)

        except Exception as e:  # noqa: F841
            self._server_card_state.set_server_loading_status(LoadState.SUCCESS)
            logger.error(f"Error restarting server: {e}")
            self._on_error(
                f"Ошибка перезагрузки сервера {self._server.name}",
            )

        else:
            self._server_card_state.set_server_loading_status(LoadState.SUCCESS)
            logger.info("Server restarted")
            self._on_success(
                f"Сервер {self._server.name} был перезагружен",
            )
            await self._refresh_servers()
