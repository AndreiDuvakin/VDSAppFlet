import flet as ft

from src.domain.notification import NotificationSettings
from src.services.notification_service import NotificationService
from src.state.app_state import AppState
from src.ui.components.progress_ring import progress_ring


def notifications_tab(
        page: ft.Page,
        state: AppState,
        service: NotificationService,
) -> ft.Control:
    page.title = "Уведомления о балансе"

    if state.notification.loading or state.notification.updating:
        return progress_ring()

    if state.notification.error and state.notification.settings is None:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED_400),
                    ft.Text(f"Ошибка: {state.notification.error}", size=16, color=ft.Colors.RED_400),
                    ft.ElevatedButton(
                        "Повторить",
                        on_click=lambda _: page.run_task(service.load_settings, state),
                        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_400),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    if not state.notification.settings:
        return ft.Text("Настройки не загружены")

    settings = state.notification.settings
    current_value_rub = settings.notify_balance_rub

    status_text = ft.Text("", size=12, color=ft.Colors.GREEN)

    async def switch_notifications(e):
        if e.control.value:
            await service.update_settings(state, 10000)

        else:
            await service.update_settings(state, 0)

    async def save_settings(e):
        try:
            new_rub = float(balance_input.value.replace(",", "."))
            if new_rub < 0:
                raise ValueError("Сумма не может быть отрицательной")
            new_copecks = NotificationSettings.from_rub(new_rub)
            await service.update_settings(state, new_copecks)

            if not state.notification.error:
                status_text.value = "✅ Настройки сохранены"
                status_text.color = ft.Colors.GREEN
            else:
                status_text.value = f"❌ {state.notification.error}"
                status_text.color = ft.Colors.RED
        except ValueError as ve:
            status_text.value = f"❌ Некорректная сумма: {ve}"
            status_text.color = ft.Colors.RED
        page.update()

    is_active_notifications = current_value_rub != 0

    switch_button = ft.Switch(
        label='Уведомлять при остатке',
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

    save_button = ft.ElevatedButton(
        "Сохранить",
        icon=ft.Icons.SAVE,
        on_click=save_settings,
        disabled=state.notification.updating or not is_active_notifications,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
        expand=True,
    )

    content = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, size=32, color=ft.Colors.BLUE_400),
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
                """Когда баланс вашего аккаунта станет ниже указанного порога, 
                на вашу электронную почту будет отправлено уведомление.""",
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
