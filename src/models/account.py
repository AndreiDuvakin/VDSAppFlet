from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountInfo:
    actdate: datetime
    country: str
    face_id: int | str
    state: int | str
    email: str
    name: str
    surname: str
    locale: str
    mobile: str
    middlename: str | None = None

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.name, self.middlename, self.surname) if p]
        return " ".join(parts) if parts else "Не указано"

    @property
    def is_active(self) -> bool:
        return self.state == 1

    @property
    def str_actdate(self) -> str | None:
        if not self.actdate:
            return None

        return self.actdate.strftime("%d.%m.%Y")

    @property
    def client_type(self) -> str:
        type_map = {
            "1": "Физическое лицо (резидент)",
            "2": "Юридическое лицо",
            "3": "Физическое лицо (нерезидент)",
        }
        return (
            type_map.get(self.face_id, "Не указано") if self.face_id else "Не указано"
        )


@dataclass
class GetAccount:
    info: AccountInfo

    def __post_init__(self):
        self.info.state = int(self.info.state)
        self.info.face_id = int(self.info.face_id)
