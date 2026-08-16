import asyncio
import logging

import flet as ft

from core.contexts import ApiClientContext, BillingPageContext
from state.billing_page_state import BillingPageState
from ui.components.empty_content import empty_content
from ui.components.progress_ring import progress_ring
from ui.components.show_message_banner import show_message_banner
from ui.pages.billing_page.tabs.payment_operations_tab import payment_operations_tab
from ui.pages.billing_page.tabs.consumption_operations_tab import (
    consumption_operations_tab,
)

logger = logging.getLogger(__name__)


@ft.component
def billing_page():
    billing_page_state, _ = ft.use_state(BillingPageState)
    api_client = ft.use_context(ApiClientContext)
    page = ft.context.page

    async def get_billing_balance():
        try:
            billing_page_state.set_is_loading(True)
            logger.info("Getting billing balance")
            balance = await api_client.billing_service.get_billing_balance()
            billing_page_state.set_balance(balance.balance)
            logger.info("Balance is loaded")

        except Exception as e:
            logger.exception(f"Error getting billing balance: {e}")
            show_message_banner(
                "Ошибка получения баланса.",
                page,
            )

        finally:
            billing_page_state.set_is_loading(False)

    if billing_page_state.is_loading:
        return progress_ring()

    if billing_page_state.balance is None and not billing_page_state.is_loading:
        asyncio.create_task(get_billing_balance())

    elif billing_page_state.balance is None:
        logger.info("Billing balance not present")
        return empty_content(
            ft.Icons.ACCOUNT_BALANCE_WALLET,
            "Нет данных о балансе",
            "Возможно при загрузке произошла ошибка",
        )

    def on_tab_changed(e):
        billing_page_state.set_current_tab_index(e.control.selected_index)

    def create_page_content():
        tabs_content = ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(
                            label="Пополнения",
                            icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
                        ),
                        ft.Tab(label="Списания", icon=ft.Icons.RECEIPT_LONG_OUTLINED),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=payment_operations_tab(),
                            expand=True,
                        ),
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=consumption_operations_tab(),
                            expand=True,
                        ),
                    ],
                ),
            ],
        )
        tabs = ft.Tabs(
            selected_index=billing_page_state.current_tab_index,
            on_change=on_tab_changed,
            length=2,
            expand=True,
            content=tabs_content,
        )

        page_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Card(
                            expand=True,
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            f"{billing_page_state.balance_rub} ₽",
                                            size=30,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            "Текущий баланс вашего аккаунта",
                                        ),
                                    ],
                                    spacing=10,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=ft.Padding.all(35),
                            ),
                            elevation=2,
                        ),
                    ],
                    expand=False,
                ),
                ft.Divider(),
                ft.Text("История платежей", size=18, weight=ft.FontWeight.BOLD),
                tabs,
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        return page_content

    return BillingPageContext(
        billing_page_state,
        create_page_content,
    )
