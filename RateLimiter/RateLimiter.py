from abc import ABC, abstractmethod


class RateLimiter(ABC):
	def __init__(self, max_requests: int, window_seconds: int):
		self._validate_config(max_requests, window_seconds)

		self.max_requests = max_requests
		self.window_seconds = window_seconds
		self.bucket_map = {}

	def set_rate_limit_config(self, max_requests: int, window_seconds: int):
		self._validate_config(max_requests, window_seconds)
		self.max_requests = max_requests
		self.window_seconds = window_seconds

	def _validate_config(self, max_requests: int, window_seconds: int):
		if max_requests <= 0:
			raise ValueError("max_requests must be greater than 0")

		if window_seconds <= 0:
			raise ValueError("window_seconds must be greater than 0")

	@abstractmethod
	def allow_request(self, user_id: str) -> bool:
		raise NotImplementedError
