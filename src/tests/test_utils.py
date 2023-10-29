"""
test_utils.py

Contains the tests for the ReddisHelper class.
"""

import unittest
from unittest.mock import patch
from ..utils import ReddisHelper


class TestReddisHelper(unittest.TestCase):
    """
    Test class for ReddisHelper.
    """

    def test_add_prefix(self):
        """
        Tests that add_prefix() adds the prefix to the key name.
        """
        assert ReddisHelper.add_prefix("test") == "account:test"
        assert ReddisHelper.add_prefix("account:test") == "account:test"
        self.assertRaises(TypeError, ReddisHelper.add_prefix, 10)

    def test_del_prefix(self):
        """
        Tests that del_prefix() removes the prefix from the key name.
        """
        assert ReddisHelper.del_prefix("test") == "test"
        assert ReddisHelper.del_prefix("account:test") == "test"

    @patch("redis.Redis")
    def test_exists(self, mock_redis):
        """
        Tests that exists() calls r.exists() with the correct parameters.
        """
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.exists("account:test")

        mock_redis_instance.exists.assert_called_with("account:test")

    @patch("redis.Redis")
    def test_get_val(self, mock_redis):
        """
        Tests that get_val() calls r.get() with the correct parameters.
        """
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.get_val("test")

        mock_redis_instance.get.assert_called_with("account:test")

    @patch("redis.Redis")
    def test_set_val(self, mock_redis):
        """
        Tests that set_val() calls r.set() with the correct parameters.
        """
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.set_val("test", 10)

        mock_redis_instance.set.assert_called_with("account:test", 10)

    @patch("redis.Redis")
    def test_accounts_list(self, mock_redis):
        """
        Tests that accounts_list() calls r.scan_iter() with the correct parameters.
        """
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.accounts_list()

        mock_redis_instance.scan_iter.assert_called_with("account:*")

    @patch("time.time", return_value=1000)
    @patch("redis.Redis")
    def test_append_refresh(self, mock_redis, mock_time):
        """
        Tests that append_refresh() calls r.xadd() with the correct parameters.
        """
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.append_refresh("test", 10, 20)

        mock_redis_instance.xadd.assert_called_with(
            "account_refresh",
            {"ts": 1000, "account": "test", "old_val": 10, "new_val": 20},
        )

        mock_time.assert_called_with()
