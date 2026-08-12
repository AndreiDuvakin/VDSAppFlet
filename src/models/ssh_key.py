from abc import ABC
from dataclasses import dataclass


@dataclass
class ServerSSHKey:
    id: int
    name: str


@dataclass
class SSHKey(ABC):
    key: str
    name: str


@dataclass
class GetSSHKey(SSHKey):
    id: int


@dataclass
class PostSSHKey(SSHKey):
    pass
