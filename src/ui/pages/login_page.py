import asyncio
import logging

import flet as ft

from src.controllers.login_page_controller import LoginPageController
from src.core.contexts import ApiClientContext, AppContext
from src.state.load_state import LoadState
from src.ui.components.progress_ring import progress_ring
from src.ui.components.show_message_banner import show_message_banner
from src.ui.components.show_simple_dialog import show_simple_dialog
from src.ui.pages.info_page import info_page

logger = logging.getLogger(__name__)


@ft.component
def login_page():
    logger.info("Initialisation login_page")

    logger.info("Calling contexts for login_page")
    app_state = ft.use_context(AppContext)
    api = ft.use_context(ApiClientContext)
    token_ref = ft.use_ref(None)
    page = ft.context.page

    if app_state.is_authenticated:
        ft.context.page.navigate("/servers")

    async def let_auth():
        token = token_ref.current.value.strip()
        await login_page_controller.lets_auth(token)

    def show_about_info():
        page.show_dialog(info_sheet)

    login_page_controller = LoginPageController(
        app_state,
        api,
        lambda title, message: show_simple_dialog(
            title,
            ft.Text(message),
            page,
        ),
        lambda message: show_message_banner(message, page),
        app_state.get_token,
        app_state.set_token,
    )

    if (
        app_state.token_secure_check_status.value == LoadState.IDLE.value
        and not app_state.token
        and not app_state.login_loading_status.value == LoadState.LOADING.value
    ):
        asyncio.create_task(login_page_controller.get_token_from_secure_storage())

    if app_state.token_secure_check_status.value == LoadState.LOADING.value:
        return progress_ring()

    logger.info("Rendering login_page")

    page_content = ft.Column(
        [
            ft.Text("VDSApp", size=25, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Вставьте токен API от вашего аккаунта VDS Selectel",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.TextField(
                label="Токен API",
                value="",
                ref=token_ref,
                password=True,
                can_reveal_password=True,
            ),
            ft.FilledButton("Войти", on_click=let_auth),
            ft.OutlinedButton("О приложении", on_click=show_about_info),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    info_sheet = ft.BottomSheet(
        content=info_page(),
        fullscreen=True,
        show_drag_handle=True,
    )

    if app_state.login_loading_status.value == LoadState.LOADING.value:
        page_content.disabled = True
        page_content.controls.insert(
            3,
            ft.ProgressBar(),
        )

    return page_content
