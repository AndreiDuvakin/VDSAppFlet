from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class BillingBalance:
    balance: int
    bonus: int
    status: str
    summ: int
    unpaid: int
    user_id: int


@dataclass
class GetBillingBalance(BillingBalance):
    pass


@dataclass
class BillingOperation:
    created: float | datetime
    desc: str
    id: int | str
    is_bonus: int | str
    price: int | str
    state: int | str
    type: int | str

    def __post_init__(self):
        self.id = int(self.id)
        self.is_bonus = int(self.is_bonus)
        self.price = int(self.price)
        self.state = int(self.state)
        self.type = int(self.type)

        if isinstance(self.created, (int, float)):
            self.created = datetime.fromtimestamp(self.created)


@dataclass
class GetBillingOperations:
    status: str
    items: List[BillingOperation] = field(
        default_factory=list,
    )


@dataclass
class BillingUsage:
    period: datetime
    resource_id: str
    plan: str
    count: int
    summ: int
