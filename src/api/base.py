import logging

from api.account_client import AccountClient
from api.notification_client import NotificationClient
from api.ssh_keys_client import SSHKeysClient
from services.account_service import AccountService
from services.notification_service import NotificationService
from services.ssh_keys_service import SSHKeysService

logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = 'https://api.vscale.io/v1/'

    def __init__(self):
        logger.info('Initializing ApiClient')

        self.token = None

        self.account_client = None
        self.account_service = None

        self.ssh_keys_client = None
        self.ssh_keys_service = None

        self.notification_client = None
        self.notification_service = None

    def init_clients(self):
        logger.info('Creating api clients and services')

        if not isinstance(self.token, str):
            logger.warning('Fail initializing: Token must be a string')
            self.delete_clients_and_services()
            raise TypeError('Token must be a string')

        logger.info('Initializing AccountService and AccountClient')
        self.account_client = AccountClient(self.token, self.BASE_URL)
        self.account_service = AccountService(self.account_client)

        logger.info('Initializing SSHKeysService and SSHKeysClient')
        self.ssh_keys_client = SSHKeysClient(self.token, self.BASE_URL)
        self.ssh_keys_service = SSHKeysService(self.ssh_keys_client)

        logger.info('Initializing NotificationService and NotificationClient')
        self.notification_client = NotificationClient(self.token, self.BASE_URL)
        self.notification_service = NotificationService(self.notification_client)

    def delete_clients_and_services(self):
        logger.info('Deleting clients and services')

        self.account_client = None
        self.account_service = None

        self.ssh_keys_client = None
        self.ssh_keys_service = None

    def set_token(self, token: str):
        logger.info('Setting token')

        self.token = token
        self.init_clients()
