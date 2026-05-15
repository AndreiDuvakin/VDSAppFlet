from dataclasses import dataclass, fields
from typing import List

from src.domain.address import Address
from src.domain.ssh_key import SSHKey


@dataclass
class Server:
    ctid: int
    name: str
    hostname: str
    status: str
    rplan: str
    location: str
    active: bool
    made_from: str
    locked: bool = False
    keys: List[SSHKey] = None
    public_address: Address | None = None
    private_address: Address | None = None

    def __post_init__(self):
        if self.keys is None:
            self.keys = []
        if isinstance(self.keys, list) and self.keys and isinstance(self.keys[0], dict):
            self.keys = [SSHKey.from_dict(k) for k in self.keys]

    @classmethod
    def from_dict(cls, data: dict):
        field_names = {f.name for f in fields(cls)}

        public_addr = Address.from_dict(data.get("public_address"))
        private_addr = Address.from_dict(data.get("private_address"))

        filtered_data = {k: v for k, v in data.items() if k in field_names}

        server = cls(
            **filtered_data,
        )

        server.public_address = public_addr
        server.private_address = private_addr

        return server

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
    def status_color(self):
        if self.status == "started":
            return "green"
        elif self.status == "stopped":
            return "orange"
        return "red"

    @property
    def get_os_name(self) -> str:
        if "ubuntu" in self.made_from.lower():
            return "Ubuntu"
        elif "debian" in self.made_from.lower():
            return "Debian"
        elif "centos" in self.made_from.lower():
            return "CentOS"
        elif "alma" in self.made_from.lower():
            return "AlmaLinux"
        return self.made_from.replace("_", " ").title()

    @property
    def get_resources_text(self) -> str:
        return f"Тариф: {self.rplan.upper()}"
