import unittest
from unittest.mock import patch
from ..utils import ReddisHelper

class TestReddisHelper(unittest.TestCase):
    def testAddPrefix(self):
        assert ReddisHelper.add_prefix("test") == "account:test"
        assert ReddisHelper.add_prefix("account:test") == "account:test"
        self.assertRaises(TypeError, ReddisHelper.add_prefix, 10)
    
    def testDelPrefix(self):
        assert ReddisHelper.del_prefix("test") == "test"
        assert ReddisHelper.del_prefix("account:test") == "test"

    @patch("redis.Redis")
    def testExists(self, mock_redis):
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.exists("account:test")

        mock_redis_instance.exists.assert_called_with("account:test")

    @patch("redis.Redis")
    def testGetVal(self, mock_redis):
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.get_val("test")
        
        mock_redis_instance.get.assert_called_with("account:test")

    @patch("redis.Redis")
    def testSetVal(self, mock_redis):
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.set_val("test", 10)
        
        mock_redis_instance.set.assert_called_with("account:test", 10)

    @patch("redis.Redis")
    def testAccountsList(self, mock_redis):
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.accounts_list()
        
        mock_redis_instance.scan_iter.assert_called_with("account:*")

    @patch("time.time", return_value=1000)
    @patch("redis.Redis")
    def testAppendRefresh(self, mock_redis, mock_time):
        mock_redis_instance = mock_redis.MagicMock()
        mock_redis.return_value = mock_redis_instance

        helper = ReddisHelper()
        helper.append_refresh("test", 10, 20)
        
        mock_redis_instance.xadd.assert_called_with("account_refresh", {"ts": 1000, "account": "test", "old_val": 10, "new_val": 20})