import asyncio
import logging
from typing import Callable

from src.api.base import ApiClient
from src.state.app_state import AppState
from src.state.load_state import LoadState
from src.state.servers_page_state import ServersPageState

logger = logging.getLogger(__name__)


class ServersPageController:
    def __init__(
        self,
        app_state: AppState,
        servers_page_state: type[ServersPageState],
        api_client: ApiClient,
        on_error: Callable[[str], None],
        is_page_active: Callable[[], bool],
    ):
        self._app_state = app_state
        self._servers_page_state = servers_page_state
        self._api_client = api_client
        self._on_error = on_error
        self._is_page_active = is_page_active

    async def get_servers_list(self) -> None:
        try:
            logger.info("Getting servers list")
            self._servers_page_state.set_servers_loading_status(LoadState.LOADING)

            servers = await self._api_client.servers_service.get_servers()
            self._app_state.set_servers_list(servers)

            logger.info("Servers list loaded")

        except Exception as e:
            self._servers_page_state.set_servers_loading_status(LoadState.ERROR)
            logger.error(f"Error getting servers list: {e}")
            self._on_error("Ошибка получения списка серверов.")

        else:
            self._servers_page_state.set_servers_loading_status(LoadState.SUCCESS)

        finally:
            logger.info("Getting servers list finished")

    async def refresh_servers(self) -> None:
        try:

            fresh_servers = await self._api_client.servers_service.get_servers()

            self._app_state.set_servers_list(fresh_servers)

            logger.info("Auto-refresh servers updated")

        except Exception as e:
            logger.error(f"Auto-refresh error: {e}")
            self._servers_page_state.set_servers_loading_status(LoadState.ERROR)

        else:
            self._servers_page_state.set_servers_loading_status(LoadState.SUCCESS)

    async def auto_refresh(self):
        try:
            while True:
                await asyncio.sleep(10)

                if not self._is_page_active:
                    break

                if (
                    self._app_state.servers is None
                    or self._servers_page_state.servers_loading_status.value
                    == LoadState.LOADING
                    or self._servers_page_state.servers_loading_status.value
                    == LoadState.ERROR
                ):
                    continue

                await self.refresh_servers()

        except asyncio.CancelledError:
            logger.info("Servers auto-refresh cancelled")
            raise

    def get_servers_list_by_tag(self):
        servers_list = self._app_state.servers or []

        if not self._servers_page_state.selected_tag_index:
            return servers_list

        try:
            selected_tag = self._app_state.tags[
                self._servers_page_state.selected_tag_index - 1
            ]
            return [
                server for server in servers_list if server.ctid in selected_tag.scalets
            ]

        except Exception as e:
            logger.error(f"Error getting selected tag: {e}")
            self._on_error("Ошибка выбора тега.")
            return servers_list

    async def repeat_loading_servers(self) -> None:
        await self.get_servers_list()
