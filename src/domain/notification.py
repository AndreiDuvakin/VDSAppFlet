from dataclasses import dataclass


@dataclass
class NotificationSettings:
    notify_balance: int
    status: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            notify_balance=data.get("notify_balance", 0),
            status=data.get("status", ""),
        )

    @property
    def notify_balance_rub(self) -> float:
        return self.notify_balance / 100

    @classmethod
    def from_rub(cls, rub: float) -> int:
        return int(rub * 100)
