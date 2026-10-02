import logging

import flet as ft

from src.controllers.backup_tile_controller import BackupTileController
from src.models.backup import GetBackup

logger = logging.getLogger(__name__)


def delete_backup_dialog(
    backup_tile_controller: BackupTileController,
    backup: GetBackup,
):
    async def confirm_delete(e):
        await backup_tile_controller.delete_backup(
            backup.id,
        )

    return ft.AlertDialog(
        title=ft.Text("Удаление бэкапа"),
        content=ft.Text(
            f"Вы уверены, что хотите удалить бэкап '{backup.name}'?\n"
            "Это действие нельзя отменить."
        ),
        actions=[
            ft.TextButton("Отмена", on_click=backup_tile_controller.pop_dialog),
            ft.FilledButton(
                "Удалить", on_click=confirm_delete, color=ft.Colors.RED_400
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
