import asyncio
import logging
from typing import Callable

from src.models.server import AddSSHKey, RenameServer
from src.models.ssh_key import GetSSHKey
from src.services.servers_service import ServersService
from src.services.ssh_keys_service import SSHKeysService
from src.state.load_state import LoadState
from src.state.server_detail_page_state import ServerDetailPageState

logger = logging.getLogger(__name__)


class ServerDetailPageController:
    def __init__(
            self,
            servers_service: ServersService,
            ssh_keys_service: SSHKeysService,
            server_detail_page_state: ServerDetailPageState,
            is_page_active: Callable[[], bool],
            show_message_banner: Callable[[str, bool | None], None],
            pop_dialog: Callable[[], None],
            show_simple_dialog: Callable[[str, str], None],
    ):
        self._servers_service = servers_service
        self._ssh_keys_service = ssh_keys_service
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
                    or self.server_detail_page_state.server_loading_status.value
                    == LoadState.LOADING.value
                    or self.server_detail_page_state.server_loading_status.value
                    == LoadState.ERROR.value
            ):
                continue

            await self._refresh_server_info()

    async def repeat_refresh_server(self):
        logger.info("Repeat auto-refresh server")
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

    async def _get_ssh_keys(self) -> list[GetSSHKey] | None:
        try:
            self.server_detail_page_state.set_server_loading_status(LoadState.LOADING)
            logger.info("Trying to get ssh keys")
            ssh_keys_list = await self._ssh_keys_service.get_ssh_keys()
            logger.info("SSH keys loaded")

            self.server_detail_page_state.set_ssh_keys_list(ssh_keys_list)
        except Exception as e:
            logger.exception(f"Error requesting SSH keys: {str(e)}")

            self._show_message_banner(
                "Ошибка получения списка SSH ключей.",
                True,
            )

        else:
            logger.info("SSH keys loaded")

        finally:
            self.server_detail_page_state.set_server_loading_status(LoadState.SUCCESS)

    async def check_keys_to_add_into_server(self):
        logger.info("Checking keys to add into server")

        if self.server_detail_page_state.ssh_keys_list is None:
            logger.info("No SSH keys loaded")
            await self._get_ssh_keys()

        if not isinstance(
                self.server_detail_page_state.server.keys, list
        ) or not isinstance(self.server_detail_page_state.ssh_keys_list, list):
            logger.info("No SSH keys loaded or created")
            self._show_message_banner(
                "Нет доступных ключей для добавления.",
                True,
            )
            return []

        current_keys_ids = [key.id for key in self.server_detail_page_state.server.keys]
        potential_new_keys = [
            key
            for key in self.server_detail_page_state.ssh_keys_list
            if key.id not in current_keys_ids
        ]

        if not potential_new_keys:
            logger.info("No ssh keys to add into server")
            self._show_message_banner(
                "Нет доступных ключей для добавления.",
                True,
            )

        logger.info("Potential new keys to add into server found")

        return potential_new_keys

    def add_selected_ssh_key(self, key_id: int):
        logger.info("Adding selected ssh key")
        self.server_detail_page_state.add_selected_ssh_key(key_id)

    def discard_selected_ssh_key(self, key_id: int):
        logger.info("Discarding selected ssh key")
        self.server_detail_page_state.discard_selected_ssh_keys(key_id)

    async def add_ssh_keys_to_server(self):
        self.pop_dialog()

        if not self.server_detail_page_state.selected_ssh_keys:
            logger.warning("No ssh keys selected")
            self._show_message_banner(
                "Выберите хотя бы один ключ",
                True,
            )

        try:
            self.server_detail_page_state.set_server_loading_status(LoadState.LOADING)

            selected_keys = list(self.server_detail_page_state.selected_ssh_keys)

            add_ssh_keys = AddSSHKey(
                keys=selected_keys,
            )

            await self._servers_service.add_new_ssh_key_to_server(
                self.server_detail_page_state.server.ctid,
                add_ssh_keys,
            )

        except Exception as e:
            logger.error(f"Error adding ssh keys to server: {e}")
            self._show_message_banner(
                "Ошибка добавления новых ключей на сервер.",
                True,
            )

        else:
            self._show_message_banner(
                "Новый SSH ключ был добавлен на сервер.",
                False,
            )
            await self._refresh_server_info()

        finally:
            self.server_detail_page_state.set_server_loading_status(LoadState.SUCCESS)
            self.server_detail_page_state.clear_selected_ssh_keys()
