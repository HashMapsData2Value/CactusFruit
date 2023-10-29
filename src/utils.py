"""
utils.py

This file contains the ReddisHelper class, which is used to help with redis operations.

"""

# pylint: disable=import-error
import time
import redis


class ReddisHelper:
    """
    A class to help with redis operations.

    ...

    Attributes
    ----------
    r : Redis
        redis client

    Methods
    -------
    add_prefix(s):
        Adds the "account:..." prefix to redis key name.

    del_prefix(s):
        Strips the "account:..." prefix of the redis key name.

    exists(k):
        Checks if value exists in redis.

    get_val(k):
        Gets the value of the key from redis.

    set_val(k, i):
        Sets the value for given key in redis.

    accounts_list():
        Returns a list of all accounts in redis.

    append_refresh(account, old_val, new_val):
        Appends a refresh event to the redis stream.

    """

    def __init__(self, host: str = "redis_service", port: int = 6379):
        """
        Initializes the redis client for the ReddisHelper object.

        Parameters
        ----------
        host : str
            The hostname of the redis service.
            Default is 'redis_service', as defined by docker-compose.yml.
        port : int
            The port of the redis service.
        """
        self.r = redis.Redis(host=host, port=port)

    @staticmethod
    def add_prefix(s: str) -> str:
        """
        Adds the "account:..." prefix to redis key name, if not already present.

        Parameters
        ----------
        s : str
            Input string key name.

        Returns
        -------
        str
        """
        if "account:" not in s:
            return "account:" + s
        return s

    @staticmethod
    def del_prefix(s: str) -> str:
        """
        Strips the "account:..." prefix from the redis key name, if present.

        Parameters
        ----------
        s : str
            Input string key name.

        Returns
        -------
        str
        """
        return s.replace("account:", "")

    def exists(self, k: str) -> bool:
        """
        Checks if the provided value exists in redis.

        Parameters
        ----------
        k : str
            The key name.

        Returns
        -------
        bool
        """
        return bool(self.r.exists(self.add_prefix(k)))

    def get_val(self, k: str) -> int:
        """
        Retrieves the value of a key in redis, which is assumed to be integer.

        Parameters
        ----------
        k : str
            The key name.

        Returns
        -------
        int
        """
        val = self.r.get(self.add_prefix(k))
        if isinstance(val, bytes):
            return int(val.decode("utf-8"))
        if val is None:
            return -1
        return int(val)

    def set_val(self, k: str, i: int) -> bool:
        """
        Sets the value of a key in redis, which is assumed to be an integer.

        Parameters
        ----------
        k : str
            The key name.
        i : int
            The integer value to set.

        Returns
        -------
        int
        """
        return bool(self.r.set(self.add_prefix(k), i))

    def accounts_list(self) -> list[str]:
        """
        Returns a list of strings of all accounts, as found with
        Redis' scan() using "account:*" as the prefix.

        Parameters
        ----------
        None

        Returns
        -------
        list[str]
        """
        accounts = []
        for key in self.r.scan_iter("account:*"):
            accounts.append(self.del_prefix(key.decode("utf-8")))
        return accounts

    def append_refresh(self, account: str, old_val: int, new_val: int) -> bytes:
        """
        Appends a refresh event to the account_refresh redis stream.

        An "account_refresh event" is emitted when the balance of a
        tracked account has changed.

        (The idea behind this is to show how these types of tracked
        events can be passed off to a message queue.)

        Parameters
        ----------
        account : str
            The account address.
        old_val : int
            The old balance of the account.
        new_val : int
            The new balance of the account.

        Returns
        -------
        bytes

        """
        return self.r.xadd(
            "account_refresh",
            {
                "ts": time.time(),
                "account": account,
                "old_val": old_val,
                "new_val": new_val,
            },
        )
