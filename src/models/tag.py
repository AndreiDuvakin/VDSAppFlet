from dataclasses import dataclass
from typing import List


@dataclass
class Tag:
    name: str


@dataclass
class GetTag(Tag):
    id: int
    scalets: List[int]


@dataclass
class PostTag(Tag):
    pass


@dataclass
class PutTag(Tag):
    domains: List[str]
