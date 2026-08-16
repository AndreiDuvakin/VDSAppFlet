import logging

import flet as ft

from core.contexts import AppContext, ApiClientContext
from ui.components.show_message_banner import show_message_banner
from ui.components.show_simple_dialog import show_simple_dialog

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

    async def lets_auth():
        logger.info("lets auth for login_page, getting token")
        token_str = token_ref.current.value.strip()

        if not token_str.strip():
            logger.warning("Token is empty, showing dialog")
            show_simple_dialog(
                "Пустой токен",
                ft.Text("Введите токен"),
                page,
            )
            return

        logger.info("Token is not empty, set token to auth state")
        api.set_token(token_str)

        try:
            app_state.set_is_login_loading(True)
            logger.info("Trying to send auth request")
            account = await api.account_service.get_account()
            app_state.login(token_str, account)
        except Exception as e:
            logger.error(f"Error auth request: {str(e)}")
            logger.info("Show error dialog")

            show_message_banner(
                "Ошибка аутентификации. Проверьте указанный токен.",
                page,
            )

        finally:
            app_state.set_is_login_loading(False)
            logger.info("Finally auth request")

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
            ft.FilledButton("Войти", on_click=lets_auth),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    if app_state.is_login_loading:
        page_content.disabled = True
        page_content.controls.insert(
            3,
            ft.ProgressBar(),
        )

    return page_content
