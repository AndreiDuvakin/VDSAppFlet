import logging
from typing import Callable

from src.api.base import ApiClient
from src.state.app_state import AppState
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


class LoginPageController:
    def __init__(
        self,
        app_state: AppState,
        api: ApiClient,
        on_message: Callable[[str, str], None],
        on_error: Callable[[str], None],
    ):
        self._app_state = app_state
        self._api = api
        self._on_message = on_message
        self._on_error = on_error

    async def lets_auth(self, token_ref):
        logger.info("lets auth for login_page, getting token")
        token_str = token_ref.current.value.strip()

        if not token_str.strip():
            logger.warning("Token is empty, showing dialog")
            self._on_message(
                "Пустой токен",
                "Введите токен",
            )
            return

        logger.info("Token is not empty, set token to auth state")
        self._api.set_token(token_str)

        try:
            self._app_state.set_login_loading_status(LoadState.LOADING)
            logger.info("Trying to send auth request")

            account = await self._api.account_service.get_account()

        except Exception as e:
            self._app_state.set_login_loading_status(LoadState.ERROR)

            logger.error(f"Error auth request: {str(e)}")
            logger.info("Show error dialog")

            self._on_error("Ошибка аутентификации. Проверьте указанный токен.")

        else:
            logger.info("Login success")
            self._app_state.set_login_loading_status(LoadState.SUCCESS)
            self._app_state.login(token_str, account)
