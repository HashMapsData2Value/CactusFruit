import redis

class ReddisHelper():
    """
    Helper class for interacting with the Reddis database.
    We store the accounts' key values with the "account:" prefix.
    This class helps 
    
    """
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.r = redis.Redis(host=host, port=port)

    def add_prefix(self, s: str) -> str:
        if "account:" not in s:
            return "account:" + s
        return s

    def del_prefix(self, s: str) -> str:
        return s.replace("account:", "")

    def exists(self, k: str) -> bool:
        return self.r.exists(self.add_prefix(k))

    def get_amt(self, k: str) -> int:
        return int(self.r.get(self.add_prefix(k)))

    def set_val(self, k: str, i: int) -> bool:
        return self.r.set(self.add_prefix(k), i)

    def accounts_list(self) -> list:
        accounts = []
        for key in self.r.scan_iter("account:*"):
            accounts.append(self.del_prefix(key))
        return accounts
