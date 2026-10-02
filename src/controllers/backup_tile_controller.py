import logging
from typing import Callable

from src.services.backups_service import BackupsService
from src.state.app_state import AppState
from src.state.backup_tile_state import BackupTileState
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


class BackupTileController:
    def __init__(
        self,
        backups_service: BackupsService,
        backup_tile_state: BackupTileState,
        app_state: AppState,
        show_message_banner: Callable[[str, bool | None], None],
        pop_dialog: Callable[[], None],
    ):
        self._backups_service = backups_service
        self._backup_tile_state = backup_tile_state
        self._app_state = app_state
        self._show_message_banner = show_message_banner
        self.pop_dialog = pop_dialog

    async def delete_backup(self, backup_id: str):
        self.pop_dialog()

        try:
            self._backup_tile_state.set_backup_loading_status(LoadState.LOADING)
            logger.info(f"Deleting backup {backup_id}")

            await self._backups_service.delete_backup(backup_id)

        except Exception as e:
            logger.error(f"Error deleting backup: {e}")
            self._show_message_banner(
                "Ошибка удаления бэкапа",
                True,
            )

        else:
            self._app_state.remove_backup_by_id(backup_id)
            logger.info(f"Backup deleted: {backup_id}")
            self._show_message_banner(
                "Бэкап был успешно удален",
                False,
            )

        finally:
            self._backup_tile_state.set_backup_loading_status(LoadState.SUCCESS)
