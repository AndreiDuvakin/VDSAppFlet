import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.models.ssh_key import GetSSHKey


def show_add_new_ssh_keys_to_server_dialog(
    server_detail_page_controller: ServerDetailPageController,
    ssh_keys: list[GetSSHKey],
):
    def handle_checkbox_change(e: ft.Event[ft.Checkbox], key_id: int) -> None:
        if e.control.value:
            server_detail_page_controller.add_selected_ssh_key(key_id)

        else:
            server_detail_page_controller.discard_selected_ssh_key(key_id)

    checkboxes_list = [
        ft.Checkbox(
            label=key.name,
            on_change=lambda e, key=key: handle_checkbox_change(e, key.id),
        )
        for key in ssh_keys
    ]

    return ft.AlertDialog(
        title=ft.Text("Добавление SSH ключа"),
        content=ft.ListView(
            controls=checkboxes_list,
        ),
        actions=[
            ft.TextButton("Отмена", on_click=server_detail_page_controller.pop_dialog),
            ft.FilledButton(
                "Добавить",
                on_click=server_detail_page_controller.add_ssh_keys_to_server,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
