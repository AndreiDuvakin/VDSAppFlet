from dataclasses import dataclass, fields


@dataclass
class Account:
    actdate: str
    country: str
    email: str
    face_id: str
    id: str
    locale: str
    middlename: str
    mobile: str
    name: str
    state: str
    surname: str

    @classmethod
    def from_dict(cls, data: dict):
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.name, self.middlename, self.surname) if p]
        return " ".join(parts) if parts else "Не указано"

    @property
    def is_active(self) -> bool:
        return self.state == "1"

    @property
    def client_type(self) -> str:
        type_map = {
            "1": "Физическое лицо (резидент)",
            "2": "Юридическое лицо",
            "3": "Физическое лицо (нерезидент)",
        }
        return type_map.get(self.face_id, "Не указано") if self.face_id else "Не указано"