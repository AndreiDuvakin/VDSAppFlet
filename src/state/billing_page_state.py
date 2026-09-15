from dataclasses import dataclass

import flet as ft

from src.models.billing import BillingOperation, BillingUsage
from src.state.load_state import LoadState


@dataclass
@ft.observable
class BillingPageState:
    balance_loading_status: LoadState = LoadState.IDLE
    billing_payment_loading_status: LoadState = LoadState.IDLE
    billing_consumption_loading_status: LoadState = LoadState.IDLE

    is_billing_consumption_loading: bool = False

    balance: int | None = None
    billing_payments: dict[int, dict[int, list[BillingOperation]]] | None = None
    billing_consumption: dict[int, dict[int, list[BillingUsage]]] | None = None

    current_tab_index: int = 0
    current_year_consumption_index: int = 0

    @property
    def balance_rub(self):
        if not isinstance(self.balance, int):
            return 0

        return round(self.balance / 100, 2)

    def set_balance_loading_status(self, loading_status: LoadState):
        self.balance_loading_status = loading_status

    def set_billing_payment_loading_status(self, loading_status: LoadState):
        self.billing_payment_loading_status = loading_status

    def set_billing_consumption_loading_status(self, loading_status: LoadState):
        self.billing_consumption_loading_status = loading_status

    def set_is_billing_consumption_loading(self, is_loading: bool):
        self.is_billing_consumption_loading = is_loading

    def set_billing_consumption(
        self, billing_consumption: dict[int, dict[int, list[BillingUsage]]]
    ):
        self.billing_consumption = billing_consumption

    def set_current_tab_index(self, index: int):
        self.current_tab_index = index

    def set_current_year_index(self, index: int):
        self.current_year_consumption_index = index

    def set_balance(self, balance: int):
        self.balance = balance

    def set_billing_payments(
        self, billing_payments: dict[int, dict[int, list[BillingOperation]]]
    ):
        self.billing_payments = billing_payments
