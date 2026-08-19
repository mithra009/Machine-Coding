class UserTier:
    def __init__(self, tier_name, request_limit, time_window):
        self.tier_name = tier_name
        self.request_limit = request_limit
        self.time_window = time_window 

    