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
    middlename: str | None = None


@dataclass
class GetAccount:
    info: AccountInfo

    def __post_init__(self):
        self.info.state = int(self.info.state)
        self.info.face_id = int(self.info.face_id)
