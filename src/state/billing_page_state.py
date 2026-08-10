from dataclasses import dataclass, field
from typing import List

import flet as ft

from models.billing import GetBillingOperations, BillingOperation


@dataclass
@ft.observable
class BillingPageState:
    is_loading: bool = False
    is_billing_payment_loading: bool = False

    balance: int | None = None
    billing_payments: dict[int, dict[int, list[BillingOperation]]] | None = None

    current_tab_index: int = 0

    @property
    def balance_rub(self):
        if not isinstance(self.balance, int):
            return 0

        return round(self.balance / 100, 2)

    def set_current_tab_index(self, index: int):
        self.current_tab_index = index

    def set_is_loading(self, is_loading: bool):
        self.is_loading = is_loading

    def set_is_billing_payment_loading(self, is_billing_payment_loading: bool):
        self.is_billing_payment_loading = is_billing_payment_loading

    def set_balance(self, balance: int):
        self.balance = balance

    def set_billing_payments(self, billing_payments: dict[int, dict[int, list[BillingOperation]]]):
        self.billing_payments = billing_payments
