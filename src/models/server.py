from dataclasses import dataclass, field

from core.constants import SERVER_STATUSES, PLANS
from models.ssh_key import ServerSSHKey


@dataclass
class ServerAddress:
    netmask: str
    gateway: str
    address: str


@dataclass
class Server:
    hostname: str
    locked: bool
    location: str
    rplan: str
    active: bool
    keys: list[ServerSSHKey]
    public_address: ServerAddress
    status: str
    made_from: str
    ctid: int
    name: str
    private_address: dict = field(default_factory=dict)

    @property
    def active_description(self) -> str:
        return "Работает" if self.active else "Не работает"

    @property
    def plan_description(self) -> str:
        return PLANS.get(
            self.rplan,
            f"Неизвестный тариф: {self.rplan}",
        )

    @property
    def public_ip(self) -> str:
        return self.public_address.address if self.public_address else "—"

    @property
    def status_text(self) -> str:
        if self.status == "started":
            return "Запущен"

        elif self.status == "stopped":
            return "Остановлен"

        elif self.status == "billing":
            return "Заблокирован (баланс)"

        return self.status.capitalize()

    @property
    def made_from_os(self) -> str:
        return self.made_from.split('_')[0]

    @property
    def status_color(self):
        if self.status == "started":
            return "green"

        elif self.status == "stopped":
            return "orange"

        return "red"

    @property
    def is_power_on(self) -> bool:
        return self.status == "started"


@dataclass
class GetServer(Server):
    pass
