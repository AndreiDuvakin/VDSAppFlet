from dataclasses import dataclass


@dataclass
class NotificationSettings:
    notify_balance: int


@dataclass
class GetNotificationSettings(NotificationSettings):
    status: str


@dataclass
class PostNotificationSettings(NotificationSettings):
    pass
