try:
    from RateLimiter.User import User
    from RateLimiter.UserTier import UserTier
    from RateLimiter.FixedWindowRateLimiter import FixedWindowRateLimiter
except ModuleNotFoundError:
    from User import User
    from UserTier import UserTier
    from FixedWindowRateLimiter import FixedWindowRateLimiter


class RateLimiterService:
    USER_MAP = {}
    USER_LIMITER_TYPE_MAP = {}
    USER_LIMITER_MAP = {}

    def __init__(self):
        self.user_map = RateLimiterService.USER_MAP
        self.user_limiter_type_map = RateLimiterService.USER_LIMITER_TYPE_MAP
        self.user_limiter_map = RateLimiterService.USER_LIMITER_MAP

    def add_user(self, name, tier: UserTier, rate_limiter_type: str = "TOKEN_BUCKET"):
        user = User(name, tier)
        self.user_map[user.user_id] = user
        self.user_limiter_type_map[user.user_id] = rate_limiter_type

        if rate_limiter_type == "FIXED_WINDOW":
            self.user_limiter_map[user.user_id] = FixedWindowRateLimiter(
                tier.request_limit,
                tier.time_window,
            )

        return user.user_id

    def get_user(self, user_id):
        return self.user_map.get(user_id, "user not found")

    def get_user_rate_limiter_type(self, user_id):
        return self.user_limiter_type_map.get(user_id, "user not found")

    def modify_user_rate_limiter_type(self, user_id, new_rate_limiter_type: str):
        if user_id in self.user_map:
            user = self.user_map[user_id]
            self.user_limiter_type_map[user_id] = new_rate_limiter_type

            if new_rate_limiter_type == "FIXED_WINDOW":
                self.user_limiter_map[user_id] = FixedWindowRateLimiter(
                    user.tier.request_limit,
                    user.tier.time_window,
                )
            elif user_id in self.user_limiter_map:
                del self.user_limiter_map[user_id]

            return True

        return False

    def get_user_tier(self, user_id):
        user = self.get_user(user_id)

        if isinstance(user, User):
            return user.tier

        return "user not found"

    def modify_user_tier(self, user_id, new_tier: UserTier):
        user = self.get_user(user_id)

        if isinstance(user, User):
            user.tier = new_tier

            limiter_type = self.user_limiter_type_map.get(user_id)
            if limiter_type == "FIXED_WINDOW":
                self.user_limiter_map[user_id] = FixedWindowRateLimiter(
                    new_tier.request_limit,
                    new_tier.time_window,
                )

            return True

        return False

    def allow_request(self, user_id):
        user = self.get_user(user_id)

        if not isinstance(user, User):
            return "user not found"

        limiter_type = self.user_limiter_type_map.get(user_id)

        if limiter_type != "FIXED_WINDOW":
            return False

        limiter = self.user_limiter_map.get(user_id)

        if limiter is None:
            limiter = FixedWindowRateLimiter(
                user.tier.request_limit,
                user.tier.time_window,
            )
            self.user_limiter_map[user_id] = limiter

        return limiter.allow_request(user_id)

    def remove_user(self, user_id):
        if user_id in self.user_map:
            del self.user_map[user_id]
            if user_id in self.user_limiter_type_map:
                del self.user_limiter_type_map[user_id]
            if user_id in self.user_limiter_map:
                del self.user_limiter_map[user_id]
            return True

        return False

