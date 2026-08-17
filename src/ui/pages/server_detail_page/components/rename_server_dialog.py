import logging

import flet as ft

from src.models.server import RenameServer
from src.ui.components.show_message_banner import show_message_banner
from src.ui.components.show_simple_dialog import show_simple_dialog

logger = logging.getLogger(__name__)


def rename_server_dialog(api_client, refresh_server, server_detail_page_state, page):
    new_name_field = ft.TextField(
        label=ft.Text("Новое название сервера"),
        value=server_detail_page_state.server.name,
    )

    def pop_dialog():
        page.pop_dialog()

    async def rename_server():
        new_name = new_name_field.value.strip()

        if not new_name:
            show_simple_dialog(
                "Некорректное название",
                ft.Text("Заполните поля с новым названием сервера"),
                page,
            )
            return

        if new_name == server_detail_page_state.server.name:
            show_simple_dialog(
                "Некорректное название",
                ft.Text("Старое и новое название должны различаться"),
                page,
            )
            return

        try:
            server_detail_page_state.set_is_server_loading(True)
            logger.info("Renaming server")

            new_name = RenameServer(
                new_name,
            )
            pop_dialog()
            await api_client.servers_service.rename_server(
                server_detail_page_state.server.ctid,
                new_name,
            )

        except Exception as e:
            logger.error(f"Error rename server: {e}")
            show_message_banner(
                "Ошибка изменения названия сервера",
                page,
            )

        else:
            logger.info("Rename server success")
            show_message_banner(
                "Название сервера изменено",
                page,
                is_error=False,
            )
            await refresh_server()

        finally:
            server_detail_page_state.set_is_server_loading(False)

    return ft.AlertDialog(
        title=ft.Text("Изменение названия сервера"),
        content=new_name_field,
        actions=[
            ft.TextButton(
                "Отмена",
                on_click=pop_dialog,
                disabled=server_detail_page_state.is_server_loading,
            ),
            ft.FilledButton(
                "Сохранить",
                on_click=rename_server,
                disabled=server_detail_page_state.is_server_loading,
            ),
        ],
    )
