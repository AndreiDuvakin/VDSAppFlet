from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class SSHKey:
    id: int
    key: Optional[str]
    name: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            key=data.get("key"),
        )
