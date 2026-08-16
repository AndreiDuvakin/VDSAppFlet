import logging

from api.account_client import AccountClient
from api.billing_client import BillingClient
from api.notification_client import NotificationClient
from api.price_client import PriceClient
from api.servers_client import ServersClient
from api.ssh_keys_client import SSHKeysClient
from api.tags_client import TagsClient
from services.account_service import AccountService
from services.billing_service import BillingService
from services.notification_service import NotificationService
from services.price_service import PriceService
from services.servers_service import ServersService
from services.ssh_keys_service import SSHKeysService
from services.tags_service import TagsService

logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = "https://api.vscale.io/v1/"

    def __init__(self):
        logger.info("Initializing ApiClient")

        self._token = None

        self._account_client = None
        self.account_service = None

        self._ssh_keys_client = None
        self.ssh_keys_service = None

        self._notification_client = None
        self.notification_service = None

        self._billing_client = None
        self.billing_service = None

        self._servers_client = None
        self.servers_service = None

        self._price_client = None
        self.price_service = None

        self._tags_client = None
        self.tags_service = None

    def init_clients(self):
        logger.info("Creating api clients and services")

        if not isinstance(self._token, str):
            logger.warning("Fail initializing: Token must be a string")
            self.delete_clients_and_services()
            raise TypeError("Token must be a string")

        logger.info("Initializing AccountService and AccountClient")
        self._account_client = AccountClient(self._token, self.BASE_URL)
        self.account_service = AccountService(self._account_client)

        logger.info("Initializing SSHKeysService and SSHKeysClient")
        self._ssh_keys_client = SSHKeysClient(self._token, self.BASE_URL)
        self.ssh_keys_service = SSHKeysService(self._ssh_keys_client)

        logger.info("Initializing NotificationService and NotificationClient")
        self._notification_client = NotificationClient(self._token, self.BASE_URL)
        self.notification_service = NotificationService(self._notification_client)

        logger.info("Initializing BillingService and BillingClient")
        self._billing_client = BillingClient(self._token, self.BASE_URL)
        self.billing_service = BillingService(self._billing_client)

        logger.info("Initializing ServersService and ServersClient")
        self._servers_client = ServersClient(self._token, self.BASE_URL)
        self.servers_service = ServersService(self._servers_client)

        logger.info("Initializing PriceService and PriceClient")
        self._price_client = PriceClient(self._token, self.BASE_URL)
        self.price_service = PriceService(self._price_client)

        logger.info("Initializing TagsService and TagsClient")
        self._tags_client = TagsClient(self._token, self.BASE_URL)
        self.tags_service = TagsService(self._tags_client)

    def delete_clients_and_services(self):
        logger.info("Deleting clients and services")

        self._account_client = None
        self.account_service = None

        self._ssh_keys_client = None
        self.ssh_keys_service = None

        self._notification_client = None
        self.notification_service = None

        self._billing_client = None
        self.billing_service = None

        self._servers_client = None
        self.servers_service = None

        self._price_client = None
        self.price_service = None

        self._tags_client = None
        self.tags_service = None

    def set_token(self, token: str):
        logger.info("Setting token")

        self._token = token
        self.init_clients()
