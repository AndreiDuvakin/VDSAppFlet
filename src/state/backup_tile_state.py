from dataclasses import dataclass

import flet as ft

from src.state.load_state import LoadState


@ft.observable
@dataclass
class BackupTileState:
    backup_loading_status: LoadState = LoadState.IDLE

    def set_backup_loading_status(self, backup_loading_status: LoadState):
        self.backup_loading_status = backup_loading_status
