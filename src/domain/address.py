from dataclasses import dataclass


@dataclass
class Address:
    address: str
    netmask: str
    gateway: str

    @classmethod
    def from_dict(cls, data: dict | None):
        if not data:
            return None
        return cls(
            address=data.get("address"),
            netmask=data.get("netmask"),
            gateway=data.get("gateway"),
        )