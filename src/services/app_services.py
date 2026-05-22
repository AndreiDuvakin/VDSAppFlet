from dataclasses import dataclass

from src.api.account_client import AccountClient
from src.api.notification_client import NotificationClient
from src.api.servers_client import ServersClient
from src.api.ssh_keys_client import SSHKeysClient
from src.services.account_service import AccountService
from src.services.notification_service import NotificationService
from src.services.servers_service import ServersService
from src.services.ssh_keys_service import SSHKeysService
from src.state.app_state import AppState


@dataclass
class AppServices:
    account_service: AccountService
    servers_service: ServersService
    ssh_keys_service: SSHKeysService
    notification_service: NotificationService

    @classmethod
    def create(cls, token: str, set_state) -> "AppServices":
        account_client = AccountClient(token)
        servers_client = ServersClient(token)
        ssh_keys_client = SSHKeysClient(token)
        notification_client = NotificationClient(token)

        return cls(
            account_service=AccountService(account_client, set_state),
            servers_service=ServersService(servers_client, set_state),
            ssh_keys_service=SSHKeysService(ssh_keys_client, set_state),
            notification_service=NotificationService(notification_client, set_state),
        )
