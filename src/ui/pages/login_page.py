import logging

import flet as ft

from src.controllers.login_page_controller import LoginPageController
from src.core.contexts import ApiClientContext, AppContext
from src.state.load_state import LoadState
from src.ui.components.show_message_banner import show_message_banner
from src.ui.components.show_simple_dialog import show_simple_dialog

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
        await login_page_controller.lets_auth(token_ref)

    login_page_controller = LoginPageController(
        app_state,
        api,
        lambda title, message: show_simple_dialog(
            title,
            ft.Text(message),
            page,
        ),
        lambda message: show_message_banner(message, page),
    )

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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    if app_state.login_loading_status.value == LoadState.LOADING.value:
        page_content.disabled = True
        page_content.controls.insert(
            3,
            ft.ProgressBar(),
        )

    return page_content
