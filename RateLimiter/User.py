import hashlib
from threading import Lock

try:
    from RateLimiter.UserTier import UserTier
except ModuleNotFoundError:
    from UserTier import UserTier


class Uid:
    def generate_uid(self, count):
        return hashlib.sha256(str(count).encode("utf-8")).hexdigest()


class User:
    USER_COUNT = 0
    _lock = Lock() 

    def __init__(self, name, tier: UserTier):
        with User._lock:
            User.USER_COUNT += 1
            current_count = User.USER_COUNT

        self.user_id = Uid().generate_uid(current_count)
        self.name = name 
        self.tier = tier 

    


    
        
