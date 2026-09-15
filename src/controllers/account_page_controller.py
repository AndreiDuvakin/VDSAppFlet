import logging
from typing import Callable

from src.models.notification import PostNotificationSettings
from src.models.ssh_key import GetSSHKey
from src.models.ssh_key import PostSSHKey
from src.services.notification_service import NotificationService
from src.services.ssh_keys_service import SSHKeysService
from src.state.account_page_state import AccountPageState
from src.state.load_state import LoadState

logger = logging.getLogger(__name__)


class AccountPageController:
    def __init__(
        self,
        account_page_state: AccountPageState,
        notification_service: NotificationService,
        ssh_keys_service: SSHKeysService,
        show_message_banner: Callable[[str, bool | None], None],
        pop_dialog: Callable[[], None],
        show_simple_dialog: Callable[[str, str], None],
    ):
        self._account_page_state = account_page_state
        self._notification_service = notification_service
        self._ssh_keys_service = ssh_keys_service
        self._show_message_banner = show_message_banner
        self.pop_dialog = pop_dialog
        self._show_simple_dialog = show_simple_dialog

    async def get_ssh_keys(self):
        try:
            logger.info("Trying to get ssh keys")
            self._account_page_state.set_ssh_keys_loading_status(LoadState.LOADING)
            ssh_keys_list = await self._ssh_keys_service.get_ssh_keys()
            logger.info("SSH keys loaded")
            self._account_page_state.set_ssh_keys(ssh_keys_list)
        except Exception as e:
            self._account_page_state.set_ssh_keys_loading_status(LoadState.ERROR)
            logger.exception(f"Error requesting SSH keys: {str(e)}")

            self._show_message_banner(
                "Ошибка получения списка SSH ключей.",
                True,
            )

        else:
            logger.info("SSH keys loaded")
            self._account_page_state.set_ssh_keys_loading_status(LoadState.SUCCESS)

    async def repeat_loading_ssh_keys(self):
        logger.info("Trying to repeat loading SSH keys")
        await self.get_ssh_keys()

    async def get_notification_settings(self):
        try:
            logger.info("Getting notification settings")
            self._account_page_state.set_notifications_loading_status(LoadState.LOADING)
            notification_settings = (
                await self._notification_service.get_notification_settings()
            )
            logger.info("Notification settings loaded")
            self._account_page_state.set_notification_balance(
                notification_settings.notify_balance
            )

        except Exception as e:
            self._account_page_state.set_notifications_loading_status(LoadState.ERROR)
            logger.exception(f"Error requesting notification settings: {str(e)}")
            self._show_message_banner(
                "Ошибка получения настроек уведомлений.",
                True,
            )

        else:
            self._account_page_state.set_notifications_loading_status(LoadState.SUCCESS)

    async def repeat_loading_notifications(self):
        logger.info("Trying to repeat loading notifications")
        await self.get_notification_settings()

    async def save_settings(self, balance_input_value):
        logger.info("Saving notification settings")
        try:
            self._account_page_state.set_notifications_loading_status(LoadState.LOADING)

            new_rub = round(float(balance_input_value.replace(",", "."))) * 100

            if new_rub < 0:
                raise ValueError

            new_notification_settings = PostNotificationSettings(
                notify_balance=new_rub,
            )

            await self._notification_service.post_notification_settings(
                new_notification_settings
            )

            logger.info("Notification settings saved")

            self._account_page_state.set_notification_balance(new_rub)

        except ValueError:
            logger.info("Invalid value notification")
            self._show_message_banner(
                "Введите корректное значение пороговой суммы.",
                True,
            )

        except Exception as e:  # noqa: F841
            logger.info(f"Error saving notification settings: {str(e)}")
            self._show_message_banner(
                "Ошибка сохранения настроек уведомлений.",
                True,
            )

        else:
            self._show_message_banner("Настройки уведомлений были обновлены.", False)

        finally:
            logger.info("Saving notification settings finnaly")
            self._account_page_state.set_notifications_loading_status(LoadState.SUCCESS)

    async def add_key(self, name_field_value, key_field_value):
        logger.info("starting ssh key creation")

        name = name_field_value.strip()
        key = key_field_value.strip()

        if not name:
            logger.warning("ssh key name field is empty")
            self._show_simple_dialog(
                "Внимание",
                "Введите название ключа",
            )
            return

        if not key:
            logger.warning("ssh key key field is empty")
            self._show_simple_dialog(
                "Внимание",
                "Введите публичный ключ",
            )
            return

        if not key.startswith(("ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp")):
            logger.warning("ssh key is not valid")
            self._show_simple_dialog(
                "Внимание",
                "Неверный формат публичного ключа",
            )
            return

        try:
            logger.debug("Trying to create ssh key")

            self._account_page_state.set_ssh_keys_loading_status(LoadState.LOADING)

            new_key = PostSSHKey(
                name=name,
                key=key,
            )

            self.pop_dialog()
            new_key = await self._ssh_keys_service.create_ssh_key(new_key)

        except Exception as e:  # noqa: F841
            logger.error(f"Error creating ssh key: {e}")
            self._show_message_banner(
                "Ошибка при добавлении ключа",
                True,
            )

        else:
            logger.info("SSH key successfully created")
            self._account_page_state.append_ssh_key(new_key)
            self._show_message_banner(
                "Новый ключ успешно добавлен",
                False,
            )

        finally:
            logger.info("Finished creating ssh key")
            self._account_page_state.set_ssh_keys_loading_status(LoadState.SUCCESS)

    async def confirm_delete(self, key: GetSSHKey):
        try:
            logger.info("trying to delete ssh key")
            self._account_page_state.set_ssh_keys_loading_status(LoadState.LOADING)
            self.pop_dialog()
            await self._ssh_keys_service.delete_ssh_key_by_id(key.id)

        except Exception as e:  # noqa: F841
            logger.error(f"Error deleting ssh key: {e}")
            self._show_message_banner(
                "Ошибка при удалении ключа",
                True,
            )
            self._account_page_state.set_ssh_keys_loading_status(LoadState.SUCCESS)

        else:
            logger.info("ssh key deleted")
            self._account_page_state.set_ssh_keys(None)
            self._show_message_banner(
                "SSH ключ успешно удален",
                False,
            )
            await self.get_ssh_keys()
