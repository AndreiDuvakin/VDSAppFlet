import asyncio
import logging

import flet as ft

from core.contexts import AppContext, ApiClientContext, ServerDetailPageContext
from state.server_detail_page_state import ServerDetailPageState
from ui.components.empty_content import empty_content
from ui.components.show_message_banner import show_message_banner
from ui.pages.server_detail_page.components.rename_server_dialog import rename_server_dialog

logger = logging.getLogger(__name__)


@ft.component
def server_detail_page():
    params = ft.use_route_params()
    ctid = params.get('ctid', None)
    page = ft.context.page

    def go_back():
        page.navigate('/servers')

    empty_page_component = ft.Column(
        [
            ft.FilledButton(
                'Вернутся назад',
                on_click=go_back,
            ),
            empty_content(
                ft.Icons.CLOUD_OFF,
                'Сервер не найден',
                'Возможно он не был загружен или указан неправильный id',
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

    if server_detail_page_state.server is None:
        server = ft.use_memo(
            lambda: app_state.get_server_by_id(ctid),
            [ctid]
        )

        if server is None:
            return empty_page_component

        server_detail_page_state.set_server(server)

    async def refresh_servers():
        try:

            fresh_server = await api_client.servers_service.get_server(server_detail_page_state.server.ctid)

            server_detail_page_state.set_server(fresh_server)

            logger.info(f"Auto-refresh server updated")

        except Exception as e:
            logger.error(f"Auto-refresh error: {e}")
            show_message_banner(
                "Ошибка обновления данных сервера.",
                page,
            )

    async def auto_refresh():
        while True:
            await asyncio.sleep(10)

            if page.route != f"/server/{ctid}":
                logger.info('Route was changed, breaking refresh')
                set_refreshing(False)
                break

            if server_detail_page_state.is_server_loading:
                continue

            await refresh_servers()

    def on_tab_changed(e):
        server_detail_page_state.set_current_tab_index(e.control.selected_index)

    ft.on_mounted(lambda: asyncio.create_task(auto_refresh()))

    refreshing, set_refreshing = ft.use_state(False)

    if not refreshing:
        print('CREATING RESRESH TASK')
        asyncio.create_task(auto_refresh())
        set_refreshing(True)

    def show_rename_server_dialog():
        page.show_dialog(
            rename_server_dialog(
                api_client,
                refresh_servers,
                server_detail_page_state,
                page,
            )
        )

    def create_page_content():
        page_bar = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back,
                ),
                ft.Text(f'Сервер {server_detail_page_state.server.name}', size=25),
                ft.IconButton(
                    ft.Icons.DRIVE_FILE_RENAME_OUTLINE,
                    on_click=show_rename_server_dialog,
                ),
                ft.Divider(),
            ],
        )

        tabs_content = ft.Column(
            [
                page_bar,
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

        tabs = ft.Tabs(
            selected_index=server_detail_page_state.current_tab_index,
            on_change=on_tab_changed,
            length=3,
            expand=True,
            content=tabs_content,
        )

        if server_detail_page_state.is_server_loading:
            tabs_content.controls.insert(
                1,
                ft.ProgressBar(),
            )

        return ft.Column(
            [
                tabs,
            ],
            expand=True,
            disabled=server_detail_page_state.is_server_loading,
        )

    return ServerDetailPageContext(
        server_detail_page_state,
        create_page_content,
    )
