from dataclasses import dataclass
from typing import List


@dataclass
class AbstractTag:
    name: str


@dataclass
class Tag(AbstractTag):
    scalets: List[int]


@dataclass
class GetTag(Tag):
    id: int


@dataclass
class PostTag(Tag):
    pass


@dataclass
class PutTag(AbstractTag):
    domains: List[str]
