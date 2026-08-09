import logging

import flet as ft

from core.contexts import AppContext, ApiClientContext

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
        return ft.ProgressRing()

    def pop_dialog():
        logger.info(f"pop dialog for login_page")
        page.pop_dialog()

    async def lets_auth():
        logger.info(f"lets auth for login_page, getting token")
        token_str = token_ref.current.value.strip()

        if not token_str.strip():
            logger.warning("Token is empty, showing dialog")
            page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Пустой токен"),
                    content=ft.Text("Введите токен"),
                    actions=[ft.TextButton("Ок", on_click=pop_dialog)],
                )
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

            action_button_style = ft.ButtonStyle(color=ft.Colors.BLACK)

            page.show_dialog(
                ft.Banner(
                    leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLACK),
                    content=ft.Text("Ошибка аутентификации. Проверьте указанный токен.", color=ft.Colors.BLACK),
                    actions=[ft.TextButton("Ок", on_click=pop_dialog, style=action_button_style)],
                    bgcolor=ft.Colors.AMBER_100,
                )
            )

        finally:
            app_state.set_is_login_loading(False)
            logger.info("Finally auth request")

    logger.info("Rendering login_page")

    page_content = ft.Column(
        [
            ft.Text('VDSApp', size=25, weight=ft.FontWeight.BOLD),
            ft.Text('Вставьте токен API от вашего аккаунта VDS Selectel', text_align=ft.TextAlign.CENTER),
            ft.TextField(
                label='Токен API',
                value="",
                ref=token_ref,
                password=True,
                can_reveal_password=True,
            ),
            ft.FilledButton('Войти', on_click=lets_auth),
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
