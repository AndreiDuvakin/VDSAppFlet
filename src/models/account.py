import datetime
from dataclasses import dataclass


@dataclass
class GetAccount:
    actdate: datetime.date
    country: str
    face_id: int
    state: int
    email: str
    name: str
    surname: str
    middlename: str | None = None
