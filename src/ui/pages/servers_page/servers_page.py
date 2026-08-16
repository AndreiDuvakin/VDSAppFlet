import asyncio
import logging

import flet as ft

from core.contexts import AppContext, ApiClientContext
from state.servers_page_state import ServersPageState
from ui.components.empty_content import empty_content
from ui.components.progress_ring import progress_ring
from ui.components.show_message_banner import show_message_banner
from ui.pages.servers_page.components.server_card import server_card

logger = logging.getLogger(__name__)


@ft.component
def servers_page():
    app_state = ft.use_context(AppContext)
    servers_page_state, _ = ft.use_state(ServersPageState)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    async def get_servers_list():
        try:
            logger.info(f"Getting servers list")
            servers_page_state.set_is_servers_loading(True)

            servers = await api_client.servers_service.get_servers()
            app_state.set_servers_list(servers)

            logger.info(f"Servers list loaded")

        except Exception as e:
            logger.error(f"Error getting servers list: {e}")
            show_message_banner(
                "Ошибка получения списка серверов.",
                page,
            )

        finally:
            logger.info(f"Getting servers list finished")
            servers_page_state.set_is_servers_loading(False)

    async def refresh_servers():
        try:

            fresh_servers = await api_client.servers_service.get_servers()

            app_state.set_servers_list(fresh_servers)

            logger.info(f"Auto-refresh servers updated")

        except Exception as e:
            logger.error(f"Auto-refresh error: {e}")

    async def auto_refresh():
        while True:
            await asyncio.sleep(10)

            if page.route != "/servers":
                break

            if not app_state.servers or servers_page_state.is_servers_loading:
                continue

            await refresh_servers()

    refresh_task: asyncio.Task | None = None

    def start_auto_refresh():
        nonlocal refresh_task
        refresh_task = asyncio.create_task(auto_refresh())

    def stop_auto_refresh():
        if refresh_task is not None and not refresh_task.done():
            refresh_task.cancel()

    ft.use_effect(start_auto_refresh, [], stop_auto_refresh)

    if servers_page_state.is_servers_loading:
        return progress_ring()

    if app_state.servers is None and not servers_page_state.is_servers_loading:
        asyncio.create_task(get_servers_list())

    if app_state.servers is None:
        return empty_content(
            ft.Icons.CLOUD_OFF,
            'Нет серверов для отображения',
            'Возможно они не были загружены',
        )

    cards = [
        server_card(server, refresh_servers)
        for server in app_state.servers
    ]

    page_content = ft.Column(
        [
            ft.Divider(),
            ft.ListView(
                controls=cards,
                expand=True,
                spacing=8,
            ),
        ],
        expand=True,
        spacing=15,
    )

    print(app_state.tags)

    if app_state.tags:
        segment_button = ft.Row(
            [
                ft.CupertinoSlidingSegmentedButton(
                    # selected_index=selected_index,
                    # on_change=handle_select_year,
                    controls=[
                        ft.Text(str(tag.name))
                        for tag in app_state.tags
                    ],
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        page_content.controls.insert(
            0,
            segment_button,
        )

    return page_content
