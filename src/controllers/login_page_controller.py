import logging
from typing import Any, Callable, Coroutine

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
        get_token: Callable[[], Coroutine[Any, Any, str | None]],
        set_token: Callable[[str], Coroutine[Any, Any, None]],
    ):
        self._app_state = app_state
        self._api = api
        self._on_message = on_message
        self._on_error = on_error
        self._get_token = get_token
        self._set_token = set_token

    async def get_token_from_secure_storage(self):
        try:
            self._app_state.set_token_secure_check_status(LoadState.LOADING)
            logger.info("Trying to get token from secure storage")
            token_str = await self._get_token()

        except Exception as e:
            logger.error(f"Error get token from secure storage: {str(e)}")
            self._on_error("Ошибка извлечения токена, нужна авторизация.")

        else:
            if isinstance(token_str, str):
                await self.lets_auth(token_str)

        finally:
            self._app_state.set_token_secure_check_status(LoadState.SUCCESS)

    async def lets_auth(self, token_str: str):
        logger.info("lets auth for login_page, getting token")

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
            await self._set_token(token_str)
            self._app_state.set_login_loading_status(LoadState.SUCCESS)
            self._app_state.login(token_str, account)
