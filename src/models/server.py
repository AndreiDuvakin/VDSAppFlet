from dataclasses import dataclass, field
from functools import cached_property

from src.core.constants import PLANS, SERVER_STATUSES
from src.models.ssh_key import ServerSSHKey
from src.utils.get_iso_image import get_iso_image


@dataclass
class ServerAddress:
    netmask: str
    gateway: str
    address: str


@dataclass
class ServerStatus:
    status: str

    @cached_property
    def status_text(self) -> str:
        return SERVER_STATUSES.get(self.status, self.status.capitalize())

    @cached_property
    def status_color(self):
        if self.status == "started":
            return "green"

        if self.status == "stopped" or self.status == "queued":
            return "orange"

        return "red"

    @cached_property
    def is_power_on(self) -> bool:
        return self.status == "started"


@dataclass
class Server(ServerStatus):
    hostname: str
    locked: bool
    location: str
    rplan: str
    active: bool
    keys: list[ServerSSHKey]
    public_address: ServerAddress
    made_from: str
    ctid: int
    name: str
    private_address: dict = field(default_factory=dict)

    @cached_property
    def beautiful_location(self) -> str:
        location = ""

        for i in self.location.upper():
            if i.isalpha():
                location += i

        return location

    @cached_property
    def active_description(self) -> str:
        return "Работает" if self.active else "Не работает"

    @cached_property
    def plan_description(self) -> str:
        return PLANS.get(
            self.rplan,
            f"Неизвестный тариф: {self.rplan}",
        )

    @cached_property
    def public_ip(self) -> str:
        return self.public_address.address if self.public_address else "—"

    @cached_property
    def made_from_os(self) -> str:
        return self.made_from.split("_")[0]

    @cached_property
    def iso_image(self) -> str:
        return get_iso_image(self.made_from)

    @cached_property
    def beautiful_name(self) -> str:
        iso_name, version, bit, _, _ = self.made_from.split("_")
        iso_name = iso_name.capitalize()
        return f"{iso_name} {version} {bit}bit"


@dataclass
class GetServer(Server):
    pass


@dataclass
class ServerLog(ServerStatus):
    id: int
    date: str


@dataclass
class GetServerLog(ServerLog):
    pass


@dataclass
class RenameServer:
    name: str


@dataclass
class AddSSHKey:
    keys: list[int]
