from dataclasses import dataclass


@dataclass
class Address:
    address: str
    netmask: str
    gateway: str