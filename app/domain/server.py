from dataclasses import dataclass, fields


@dataclass
class Server:
    ctid: int
    name: str
    status: str
    rplan: str
    location: str
    active: bool
    hostname: str

    @classmethod
    def from_dict(cls, data: dict):
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)