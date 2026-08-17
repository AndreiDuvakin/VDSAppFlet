import asyncio
import logging

import flet as ft

from src.core.contexts import AccountPageContext, ApiClientContext
from src.models.notification import PostNotificationSettings
from src.ui.components.empty_content import empty_content
from src.ui.components.show_message_banner import show_message_banner

logger = logging.getLogger(__name__)


@ft.component
def notifications_tab():
    logger.info("Initializing notifications_tab")

    account_page_state = ft.use_context(AccountPageContext)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    async def get_notification_settings():
        try:
            logger.info("Getting notification settings")
            account_page_state.set_is_loading_notifications(True)
            notification_settings = (
                await api_client.notification_service.get_notification_settings()
            )
            logger.info("Notification settings loaded")
            account_page_state.set_notification_balance(
                notification_settings.notify_balance
            )

        except Exception as e:
            logger.exception(f"Error requesting notification settings: {str(e)}")
            show_message_banner(
                "Ошибка получения настроек уведомлений.",
                page,
            )

        finally:
            account_page_state.set_is_loading_notifications(False)

    async def switch_notifications(e):
        if e.control.value:
            account_page_state.set_notification_balance(10000)

        else:
            account_page_state.set_notification_balance(0)

    async def save_settings(e):
        logger.info("Saving notification settings")
        try:
            account_page_state.set_is_loading_notifications(True)

            new_rub = round(float(balance_input.value.replace(",", "."))) * 100

            if new_rub < 0:
                raise ValueError

            new_notification_settings = PostNotificationSettings(
                notify_balance=new_rub,
            )

            await api_client.notification_service.post_notification_settings(
                new_notification_settings
            )

            logger.info("Notification settings saved")

            account_page_state.set_notification_balance(new_rub)

        except ValueError:
            logger.info("Invalid value notification")
            show_message_banner(
                "Введите корректное значение пороговой суммы.",
                page,
            )

        except Exception as e:  # noqa: F841
            logger.info(f"Error saving notification settings: {str(e)}")
            show_message_banner(
                "Ошибка сохранения настроек уведомлений.",
                page,
            )

        else:
            show_message_banner(
                "Настройки уведомлений были обновлены.",
                page,
                is_error=False,
            )

        finally:
            logger.info("Saving notification settings finnaly")
            account_page_state.set_is_loading_notifications(False)

    if (
        account_page_state.notification_settings is None
        and not account_page_state.is_loading_notifications
    ):
        logger.info("Notification settings not loaded, starting loading")
        asyncio.create_task(get_notification_settings())

    if account_page_state.notification_settings is None:
        logger.info("Notification settings not present")
        return empty_content(
            ft.Icons.NOTIFICATION_IMPORTANT,
            "Нет данных об уведомлениях",
            "Возможно при загрузке произошла ошибка",
        )

    logger.info("Notification settings loaded, displaying")

    current_value_rub = account_page_state.notification_settings / 100

    is_active_notifications = current_value_rub != 0

    switch_button = ft.Switch(
        label="Уведомлять при остатке",
        value=is_active_notifications,
        on_change=switch_notifications,
    )

    balance_input = ft.TextField(
        label="Порог баланса (рубли)",
        value=str(current_value_rub),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix="₽",
        expand=True,
        text_size=16,
        input_filter=ft.InputFilter(regex_string=r"[0-9]", allow=True),
        disabled=not is_active_notifications,
    )

    save_button = ft.FilledButton(
        "Сохранить",
        icon=ft.Icons.SAVE,
        on_click=save_settings,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
        expand=True,
    )

    content = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.NOTIFICATIONS_ACTIVE,
                            size=32,
                            color=ft.Colors.BLUE_400,
                        ),
                        ft.Text(
                            "Уведомления об исчерпании баланса",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                            max_lines=2,
                            no_wrap=False,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.Margin.only(bottom=10),
            ),
            switch_button,
            ft.Text(
                "Когда баланс вашего аккаунта станет ниже указанного порога "
                "на вашу электронную почту будет отправлено уведомление.",
                size=14,
                selectable=True,
                color=ft.Colors.GREY_700,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            balance_input,
            save_button,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
    )

    return ft.Container(
        content=ft.Card(
            content=ft.Container(
                content=content,
                padding=20,
            ),
            elevation=3,
            margin=ft.Margin.all(16),
        ),
        expand=True,
    )
