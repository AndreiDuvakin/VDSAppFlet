import asyncio
import logging
from typing import Callable

from src.models.server import RenameServer
from src.services.servers_service import ServersService
from src.state.server_detail_page_state import ServerDetailPageState
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


class ServerDetailPageController:
    def __init__(
            self,
            servers_service: ServersService,
            server_detail_page_state: ServerDetailPageState,
            is_page_active: Callable[[], bool],
            show_message_banner: Callable[[str, bool | None], None],
            pop_dialog: Callable[[], None],
            show_simple_dialog: Callable[[str, str], None],
    ):
        self._servers_service = servers_service
        self.server_detail_page_state = server_detail_page_state
        self._is_page_active = is_page_active
        self._show_message_banner = show_message_banner
        self.pop_dialog = pop_dialog
        self._show_simple_dialog = show_simple_dialog

    async def _refresh_server_info(self):
        try:

            fresh_server = await self._servers_service.get_server(
                self.server_detail_page_state.server.ctid
            )

            self.server_detail_page_state.set_server(fresh_server)

        except Exception as e:
            self.server_detail_page_state.set_server_loading_status(LoadState.ERROR)
            logger.error(f"Auto-refresh error: {e}")
            self._show_message_banner(
                "Ошибка обновления данных сервера.",
                True,
            )

        else:
            logger.info("Auto-refresh server updated")
            self.server_detail_page_state.set_server_loading_status(LoadState.SUCCESS)

    async def auto_refresh(self):
        while True:
            await asyncio.sleep(10)

            if not self._is_page_active():
                logger.info("Route was changed, breaking refresh")
                break

            if (
                    self.server_detail_page_state.server is None
                    or self.server_detail_page_state.server_loading_status.value == LoadState.LOADING.value
                    or self.server_detail_page_state.server_loading_status.value == LoadState.ERROR.value
            ):
                continue

            await self._refresh_server_info()

    async def repeat_refresh_server(self):
        logger.info(f"Repeat auto-refresh server")
        self.server_detail_page_state.set_server_loading_status(LoadState.LOADING)
        await self._refresh_server_info()

    async def rename_server(self, new_name):
        if not new_name:
            self._show_simple_dialog(
                "Некорректное название",
                "Заполните поля с новым названием сервера",
            )
            return

        if new_name == self.server_detail_page_state.server.name:
            self._show_simple_dialog(
                "Некорректное название",
                "Старое и новое название должны различаться",
            )
            return

        try:
            self.server_detail_page_state.set_server_loading_status(LoadState.LOADING)
            logger.info("Renaming server")

            new_name = RenameServer(
                new_name,
            )
            self.pop_dialog()
            await self._servers_service.rename_server(
                self.server_detail_page_state.server.ctid,
                new_name,
            )

        except Exception as e:
            self.server_detail_page_state.set_server_loading_status(LoadState.SUCCESS)
            logger.error(f"Error rename server: {e}")
            self._show_message_banner(
                "Ошибка изменения названия сервера",
                True,
            )

        else:
            self.server_detail_page_state.set_server_loading_status(LoadState.SUCCESS)
            logger.info("Rename server success")
            self._show_message_banner(
                "Ошибка изменения названия сервера",
                False,
            )
            await self._refresh_server_info()
