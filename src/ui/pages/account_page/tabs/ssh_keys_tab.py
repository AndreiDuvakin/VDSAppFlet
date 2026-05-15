import flet as ft

from src.services.ssh_keys_service import SSHKeysService
from src.state.app_state import AppState
from src.ui.components.progress_ring import progress_ring


def ssh_keys_tab(
        page: ft.Page,
        state: AppState,
        service: SSHKeysService,
) -> ft.Control:
    page.title = 'SSH Ключи'

    if state.ssh_keys.loading:
        return progress_ring()

    if state.ssh_keys.error:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED_400),
                    ft.Text(f"Ошибка: {state.ssh_keys.error}", size=16, color=ft.Colors.RED_400),
                    ft.ElevatedButton(
                        "Повторить",
                        on_click=lambda _: page.run_task(service.load_ssh_keys, state),
                        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_400),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    def show_delete_dialog(key_id: int, key_name: str):
        def confirm_delete(e):
            page.run_task(service.delete_ssh_key, state, key_id)
            page.pop_dialog()

        dialog = ft.AlertDialog(
            title=ft.Text("Удаление SSH ключа"),
            content=ft.Text(f"Вы уверены, что хотите удалить ключ '{key_name}'?\nЭто действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: page.pop_dialog()),
                ft.ElevatedButton("Удалить", on_click=confirm_delete, color=ft.Colors.RED_400),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialog)

    def show_add_dialog():
        name_field = ft.TextField(
            label="Название ключа",
            hint_text="Например: Мой домашний ПК",
            max_length=255,
        )
        key_field = ft.TextField(
            label="Публичный ключ",
            hint_text="ssh-rsa AAAAB3NzaC1yc2E...",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        def add_key(e):
            name = name_field.value.strip()
            key = key_field.value.strip()

            if not name:
                name_field.error_text = "Введите название ключа"
                page.update()
                return
            if not key:
                key_field.error_text = "Введите публичный ключ"
                page.update()
                return
            if not key.startswith(("ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp")):
                key_field.error_text = "Неверный формат публичного ключа"
                page.update()
                return

            page.run_task(service.add_ssh_key, state, name, key)
            page.pop_dialog()

        dialog = ft.AlertDialog(
            title=ft.Text("Добавление SSH ключа"),
            content=ft.Column(
                [
                    ft.Text("Добавьте новый публичный SSH ключ для доступа к серверам."),
                    ft.Divider(),
                    name_field,
                    key_field,
                ],
                width=500,
                height=300,
                spacing=15,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: page.pop_dialog()),
                ft.ElevatedButton("Добавить", on_click=add_key, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialog)

    add_button = ft.Container(
        content=ft.ElevatedButton(
            "Добавить SSH ключ",
            icon=ft.Icons.ADD,
            on_click=lambda _: show_add_dialog(),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE,
            ),
        ),
        padding=ft.Padding.only(bottom=15),
    )

    if not state.ssh_keys.items:
        return ft.Column(
            [
                add_button,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.VPN_KEY, size=64, color=ft.Colors.GREY_400),
                            ft.Text("Нет SSH ключей", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Добавьте публичный SSH ключ для доступа к серверам",
                                size=14,
                                color=ft.Colors.GREY_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            expand=True,
        )

    ssh_keys_list = ft.ListView(
        expand=True,
        spacing=10,
        controls=[
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VPN_KEY, color=ft.Colors.BLUE_400, size=24),
                                    ft.Text(key.name, size=16, weight=ft.FontWeight.BOLD, expand=True),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_400,
                                        tooltip="Удалить ключ",
                                        on_click=lambda e, kid=key.id, kname=key.name: show_delete_dialog(kid, kname),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Divider(height=5, thickness=0.5),
                            ft.Text(f"ID: {key.id}", size=10, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.all(15),
                ),
                elevation=2,
            ) for key in state.ssh_keys.items
        ],
    )

    return ft.Column(
        [
            add_button,
            ssh_keys_list,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
