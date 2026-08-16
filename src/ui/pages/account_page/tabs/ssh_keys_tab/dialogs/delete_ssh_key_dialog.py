import logging

import flet as ft

from ui.components.show_message_banner import show_message_banner

logger = logging.getLogger(__name__)


def delete_ssh_key_dialog(key, page, account_page_state, api_client):
    logger.info("Open delete_ssh_key_dialog")

    async def confirm_delete(e):
        try:
            logger.info("trying to delete ssh key")
            account_page_state.set_is_loading_ssh_keys(True)
            pop_dialog()
            await api_client.ssh_keys_service.delete_ssh_key_by_id(key.id)

        except Exception as e:  # noqa: F841
            logger.error(f"Error deleting ssh key: {e}")
            show_message_banner(
                "Ошибка при удалении ключа",
                page,
            )

        else:
            logger.info("ssh key deleted")
            account_page_state.set_ssh_keys(None)
            show_message_banner(
                "SSH ключ успешно удален",
                page,
                is_error=False,
            )

        finally:
            logger.info("finally delete ssh key")
            account_page_state.set_is_loading_ssh_keys(False)

    def pop_dialog():
        page.pop_dialog()

    dialog = ft.AlertDialog(
        title=ft.Text("Удаление SSH ключа"),
        content=ft.Text(
            f"Вы уверены, что хотите удалить ключ '{key.name}'?\n"
            "Это действие нельзя отменить."
        ),
        actions=[
            ft.TextButton("Отмена", on_click=pop_dialog),
            ft.FilledButton(
                "Удалить", on_click=confirm_delete, color=ft.Colors.RED_400
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog
