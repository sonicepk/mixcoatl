"""
mixcoatl.admin.account
----------------------

Implements access to the enStratus Account API
"""
from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.utils import camelize
import json

class Account(Resource):
    """An account object represents an enStratus account held by an enStratus customer."""

    PATH = 'admin/Account'
    COLLECTION_NAME = 'accounts'
    PRIMARY_KEY = 'account_id'

    def __init__(self, account_id = None, *args, **kwargs):
        Resource.__init__(self)
        self.__account_id = account_id

    @property
    def account_id(self):
        """`int` - The unique ID of this account"""
        return self.__account_id

    @lazy_property
    def alert_configuration(self):
        """`dict` - The configuration of alert preferences for this account."""
        return self.__alert_configuration

    @lazy_property
    def billing_system_id(self):
        """`int` - The ID associated with this account that may appear on invoices."""
        return self.__billing_system_id

    @lazy_property
    def cloud_subscription(self):
        """`dict` or `None` -- Information about the cloud for this account"""
        return self.__cloud_subscription

    @lazy_property
    def configured(self):
        """`bool` - Has this account has been tied to an account with a cloud provider"""
        return self.__configured

    @lazy_property
    def customer(self):
        """`dict` - The enStratus customer record to which this account belongs"""
        return self.__customer

    @lazy_property
    def default_budget(self):
        """The unique id of the billing code that is the default for discovered resources"""
        return self.__default_budget

    @lazy_property
    def dns_automation(self):
        """Does this account subscribe to dns_automation?"""
        return self.__dns_automation

    @lazy_property
    def name(self):
        """`str` - User-friendly name used to identify the account"""
        return self.__name

    @lazy_property
    def owner(self):
        """`dict` - user who owns this account"""
        return self.__owner

    @lazy_property
    def plan_id(self):
        """`int` - pricing plan associated with this account"""
        return self.__plan_id

    @lazy_property
    def provisioned(self):
        """`bool` - Is this account in goodstanding and managed by enStratus"""
        return self.__provisioned

    @lazy_property
    def status(self):
        """`str` - The current account payment status"""
        return self.__status

    @lazy_property
    def subscribed(self):
        """`bool` - If the account is configured and the cloud account is working with enStratus"""
        return self.__subscribed


    @classmethod
    def all(cls, keys_only = False, **kwargs):
        """Get all accounts

        >>> Account.all(detail='basic')
        [{'account_id':12345,....}]

        >>> Account.all(keys_only=True)
        [12345]

        :param keys_only: Only return `account_id` instead of `Account` objects
        :type keys_only: bool.
        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :param cloud_id: Only show accounts tied to the given cloud
        :type cloud_id: int.
        :returns: `list` of :class:`Account` or :attr:`account_id`
        :raises: :class:`AccountException`
        """

        r = Resource(cls.PATH)
        if 'detail' in kwargs:
            r.request_details = kwargs['detail']
        else:
            r.request_details = 'basic'

        if 'cloud_id' in kwargs:
            params = {'cloudId': kwargs['cloud_id']}
        else:
            params = {}

        c = r.get(params=params)
        if r.last_error is None:
            if keys_only is True:
                return [i[camelize(cls.PRIMARY_KEY)] for i in c[cls.COLLECTION_NAME]]
            else:
                return [cls(i[camelize(cls.PRIMARY_KEY)]) for i in c[cls.COLLECTION_NAME]]
        else:
            raise AccountException(r.last_error)

class AccountException(BaseException): pass
