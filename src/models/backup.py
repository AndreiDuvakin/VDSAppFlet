from dataclasses import dataclass
from functools import cached_property


@dataclass
class BaseBackup:
    name: str


@dataclass
class BackupStatus:
    status: str

    @cached_property
    def status_text(self) -> str:
        match self.status:
            case "defining":
                return "Создана запись в БД"

            case "creating":
                return "Создается"

            case "uploading":
                return "Загрузка в файловую систему"

            case "finished":
                return "Создана"

        return self.status.capitalize()


@dataclass
class Backup(BaseBackup, BackupStatus):
    id: str
    location: str
    scalet: int
    size: int
    template: str
    created: str
    locked: bool
    active: bool
    is_deleted: bool

    @cached_property
    def beautiful_location(self) -> str:
        location = ""

        for i in self.location.upper():
            if i.isalpha():
                location += i

        return location


@dataclass
class GetBackup(Backup):
    pass


@dataclass
class PostBackup(BaseBackup):
    pass
