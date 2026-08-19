import time
from threading import Lock

try:
    from RateLimiter.RateLimiter import RateLimiter
except ModuleNotFoundError:
    from RateLimiter import RateLimiter


class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_seconds: int):
        super().__init__(max_requests, window_seconds)
        self._lock = Lock()

    def allow_request(self, user_id: str) -> bool:
        now = int(time.time())

        with self._lock:
            state = self.bucket_map.get(user_id)

            if state is None:
                self.bucket_map[user_id] = {
                    "window_start": now,
                    "count": 1,
                }
                return True

            window_start = state["window_start"]
            count = state["count"]

            if now - window_start >= self.window_seconds:
                state["window_start"] = now
                state["count"] = 1
                return True

            if count < self.max_requests:
                state["count"] += 1
                return True

            return False
