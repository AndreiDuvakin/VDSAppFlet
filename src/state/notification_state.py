from dataclasses import dataclass

import flet as ft

from src.domain.notification import NotificationSettings


@ft.observable
@dataclass
class NotificationState:
    settings: NotificationSettings | None = None
    loading: bool = False
    error: str | None = None
    updating: bool = False
