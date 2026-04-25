import time
from collections import deque

class RateLimitGuard:
    def __init__(self, max_calls=8, window=1.0):
        self.max_calls = max_calls
        self.window = window
        self.calls = deque()

    def allow(self):
        now = time.time()
        while self.calls and now - self.calls[0] > self.window:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True
