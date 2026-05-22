import flet as ft

from src.domain.server import Server
from src.services.app_services import AppServices
from src.ui.components.progress_ring import progress_ring
from src.state.app_state import AppState
from src.ui.components.show_simple_dialog import show_simple_dialog


def select_ssh_key_to_add(
        server: Server,
        services: AppServices,
        state: AppState,
        page: ft.Page
):
    selected_keys = []

    def on_key_toggle(key_id: int, e):
        if e.control.value:
            if key_id not in selected_keys:
                selected_keys.append(key_id)
        else:
            if key_id in selected_keys:
                selected_keys.remove(key_id)

    def add_keys(e):
        if not selected_keys:
            show_simple_dialog(
                "Внимание",
                ft.Text("Выберите хотя бы один ключ"),
                page,
            )
            return

        page.pop_dialog()
        page.run_task(
            services.servers_service.add_ssh_key,
            state,
            server.ctid,
            selected_keys,
        )

    if not state.ssh_keys.items and not state.ssh_keys.loading:
        page.run_task(services.ssh_keys_service.load_ssh_keys, state)

    if state.ssh_keys.loading:
        content = ft.Container(
            content=progress_ring(),
            alignment=ft.Alignment.CENTER,
            expand=True,
            height=300,
        )

    elif not state.ssh_keys.items:
        content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.VPN_KEY, size=48, color=ft.Colors.GREY_400),
                ft.Text("Нет доступных SSH ключей", size=18),
                ft.Text("Добавьте ключ в разделе Аккаунт", color=ft.Colors.GREY_500),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )
    else:

        server_keys_ids = list(map(
            lambda key: key.id,
            server.keys,
        ))

        filtered_keys = list(filter(
            lambda key: key.id not in server_keys_ids,
            state.ssh_keys.items,
        ))

        content = ft.ListView(
            expand=True,
            spacing=8,
            height=320,
            controls=[
                ft.Checkbox(
                    label=f"{key.name} (ID: {key.id})",
                    value=False,
                    on_change=lambda e, kid=key.id: on_key_toggle(kid, e),
                ) for key in filtered_keys
            ]
        )

    dialog = ft.AlertDialog(
        title=ft.Text("Добавить SSH ключ на сервер"),
        content=ft.Container(
            content=ft.Column([
                ft.Text(f"Сервер: {server.name or server.hostname} (#{server.ctid})",
                        size=15, color=ft.Colors.GREY_700),
                ft.Divider(),
                content,
            ], spacing=10),
            width=400,
            height=420,
        ),
        actions=[
            ft.TextButton("Отмена", on_click=lambda _: page.pop_dialog()),
            ft.FilledButton(
                "Добавить",
                icon=ft.Icons.ADD,
                on_click=add_keys,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.show_dialog(dialog)
