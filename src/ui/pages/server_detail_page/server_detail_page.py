import asyncio
import logging

import flet as ft

from src.controllers.server_detail_page_controller import ServerDetailPageController
from src.core.contexts import ApiClientContext, AppContext, ServerDetailPageContext
from src.state.load_state import LoadState
from src.state.server_detail_page_state import ServerDetailPageState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.components.show_message_banner import show_message_banner
from src.ui.pages.server_detail_page.components.rename_server_dialog import (
    rename_server_dialog,
)
from src.ui.pages.server_detail_page.tabs.server_properties_tab import (
    server_properties_tab,
)
from src.ui.widgets.price_widget import price_widget
from src.ui.components.show_simple_dialog import show_simple_dialog

logger = logging.getLogger(__name__)


@ft.component
def server_detail_page():
    params = ft.use_route_params()
    ctid = params.get("ctid", None)
    page = ft.context.page

    def go_back():
        page.navigate("/servers")

    empty_page_component = ft.Column(
        [
            ft.FilledButton(
                "Вернутся назад",
                on_click=go_back,
            ),
            empty_content(
                ft.Icons.CLOUD_OFF,
                "Сервер не найден",
                "Возможно он не был загружен или указан неправильный id",
            ),
        ]
    )

    if ctid is None:
        return empty_page_component

    try:
        ctid = int(ctid)

    except ValueError:
        return empty_page_component

    app_state = ft.use_context(AppContext)
    server_detail_page_state, _ = ft.use_state(ServerDetailPageState)
    api_client = ft.use_context(ApiClientContext)

    server = ft.use_memo(
        lambda: app_state.get_server_by_id(ctid),
        [ctid, app_state.servers],
    )

    if server_detail_page_state.server is None:
        if server is None:
            return empty_page_component

        server_detail_page_state.set_server(server)

    server_detail_page_controller = ServerDetailPageController(
        api_client.servers_service,
        server_detail_page_state,
        lambda: page.route == f"/server/{ctid}",
        lambda message, is_error=False: show_message_banner(message, page, is_error),
        lambda: page.pop_dialog(),
        lambda title, message: show_simple_dialog(title, ft.Text(message), page),
    )

    if server_detail_page_state.server_loading_status.value == LoadState.ERROR.value:
        return ft.Column(
            [
                error_content(
                    "Не удалось загрузить информацию о сервере",
                    "Проверьте подключение к интернету или попробуйте ещё раз.",
                    server_detail_page_controller.repeat_refresh_server,
                ),
                ft.Button(
                    "Вернутся на главную",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back,
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    is_server_detail_page_loading = server_detail_page_state.server_loading_status.value == LoadState.LOADING.value

    def on_tab_changed(e):
        server_detail_page_state.set_current_tab_index(e.control.selected_index)

    refresh_task: asyncio.Task | None = None

    def start_auto_refresh():
        nonlocal refresh_task
        refresh_task = asyncio.create_task(server_detail_page_controller.auto_refresh())

    def stop_auto_refresh():
        if refresh_task is not None and not refresh_task.done():
            refresh_task.cancel()

    ft.use_effect(start_auto_refresh, [ctid], stop_auto_refresh)

    def show_rename_server_dialog():
        page.show_dialog(
            rename_server_dialog(
                server_detail_page_controller,
            )
        )

    def create_page_content():
        page_bar = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back,
                ),
                ft.Text(f"Сервер {server_detail_page_state.server.name}", size=25),
                ft.IconButton(
                    ft.Icons.DRIVE_FILE_RENAME_OUTLINE,
                    on_click=show_rename_server_dialog,
                ),
                ft.Divider(),
            ],
        )

        plan_description = ft.Row(
            [
                ft.Text(server.plan_description, size=15),
                price_widget(server.rplan),
            ]
        )

        tabs_content = ft.Column(
            [
                page_bar,
                ft.Row(
                    [
                        ft.Image(server.iso_image, width=80, height=80),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.LOCATION_ON,
                                            color=ft.Colors.BLUE_400,
                                        ),
                                        ft.Text(
                                            server.beautiful_location,
                                            weight=ft.FontWeight.W_500,
                                            expand=True,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.SETTINGS_SYSTEM_DAYDREAM,
                                            color=ft.Colors.CYAN_400,
                                        ),
                                        ft.Text(
                                            server.beautiful_name,
                                            weight=ft.FontWeight.W_500,
                                            expand=True,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.MEMORY,
                                            color=ft.Colors.BLUE_GREY_400,
                                        ),
                                        plan_description,
                                    ],
                                    spacing=8,
                                ),
                            ],
                        ),
                    ],
                ),
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Параметры сервера", icon=ft.Icons.DNS),
                        ft.Tab(label="История", icon=ft.Icons.HISTORY),
                        ft.Tab(label="Бэкапы", icon=ft.Icons.BACKUP),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            expand=True,
                            content=server_properties_tab(),
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            expand=True,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            expand=True,
                        ),
                    ],
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        )

        if is_server_detail_page_loading:
            tabs_content.controls.insert(
                1,
                ft.ProgressBar(),
            )

        tabs = ft.Tabs(
            selected_index=server_detail_page_state.current_tab_index,
            on_change=on_tab_changed,
            length=3,
            expand=True,
            content=tabs_content,
        )

        return ft.Column(
            [
                tabs,
            ],
            expand=True,
            disabled=is_server_detail_page_loading,
        )

    return ServerDetailPageContext(
        server_detail_page_state,
        create_page_content,
    )
