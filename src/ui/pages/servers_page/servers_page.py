import asyncio
import logging

import flet as ft

from src.controllers.servers_page.servers_page_controller import ServersPageController
from src.core.contexts import ApiClientContext, AppContext
from src.state.load_state import LoadState
from src.state.servers_page_state import ServersPageState
from src.ui.components.empty_content import empty_content
from src.ui.components.error_content import error_content
from src.ui.components.progress_ring import progress_ring
from src.ui.components.show_message_banner import show_message_banner
from src.ui.pages.servers_page.components.server_card import server_card

logger = logging.getLogger(__name__)


@ft.component
def servers_page():
    app_state = ft.use_context(AppContext)
    servers_page_state, _ = ft.use_state(ServersPageState)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    servers_page_controller = ServersPageController(
        app_state,
        servers_page_state,
        api_client.servers_service,
        lambda message: show_message_banner(message, page),
        lambda: page.route == "/servers",
    )

    refresh_task: asyncio.Task | None = None

    def start_auto_refresh():
        logger.info("Start auto-refresh servers list")
        nonlocal refresh_task
        refresh_task = asyncio.create_task(servers_page_controller.auto_refresh())

    def stop_auto_refresh():
        if refresh_task is not None and not refresh_task.done():
            refresh_task.cancel()

    ft.use_effect(start_auto_refresh, [], stop_auto_refresh)

    if servers_page_state.servers_loading_status.value == LoadState.LOADING.value:
        return progress_ring()

    if servers_page_state.servers_loading_status.value == LoadState.ERROR.value:
        return error_content(
            "Не удалось загрузить серверы",
            "Проверьте подключение к интернету или попробуйте ещё раз.",
            servers_page_controller.repeat_loading_servers,
        )

    if (
        app_state.servers is None
        and servers_page_state.servers_loading_status.value == LoadState.IDLE.value
    ):
        logger.info("On-mount servers loading starting")
        asyncio.create_task(servers_page_controller.get_servers_list())

    if app_state.servers is None:
        return empty_content(
            ft.Icons.CLOUD_OFF,
            "Нет серверов для отображения",
            "Возможно они не были загружены",
        )

    servers_list = ft.use_memo(
        servers_page_controller.get_servers_list_by_tag,
        [
            app_state.servers,
            servers_page_state.selected_tag_index,
            app_state.tags,
        ],
    )

    cards = [
        server_card(server, servers_page_controller.refresh_servers)
        for server in servers_list
    ]

    page_content = ft.Column(
        [
            ft.ListView(
                controls=cards,
                expand=True,
                spacing=8,
            ),
        ],
        expand=True,
        spacing=15,
    )

    def handle_select_tag(e: ft.Event[ft.CupertinoSlidingSegmentedButton]):
        selected_index = e.control.selected_index
        servers_page_state.set_selected_tag_index(selected_index)

    if app_state.tags:
        tags = [ft.Text(str(tag.name)) for tag in app_state.tags]

        tags.insert(0, ft.Text("Все"))

        segment_button = ft.Row(
            [
                ft.Text("Теги серверов:"),
                ft.CupertinoSlidingSegmentedButton(
                    selected_index=servers_page_state.selected_tag_index,
                    on_change=handle_select_tag,
                    controls=tags,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page_content.controls.insert(
            0,
            segment_button,
        )
        page_content.controls.insert(
            1,
            ft.Divider(),
        )

    return page_content
