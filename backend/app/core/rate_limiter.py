# app/core/rate_limiter.py
import time
from collections import defaultdict, deque
from typing import Deque, Dict


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        request_times = self.requests[client_id]

        # Remove old requests
        while request_times and request_times[0] < window_start:
            request_times.popleft()

        if len(request_times) >= self.max_requests:
            return False

        request_times.append(now)
        return True
