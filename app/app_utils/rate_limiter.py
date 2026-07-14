# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import os
import logging
import threading

logger = logging.getLogger(__name__)

class TokenBucket:
    """A thread-safe token bucket rate limiter for requests."""

    def __init__(self, capacity: float, refill_rate: float):
        """
        Args:
            capacity: Maximum token capacity.
            refill_rate: Tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_update = time.monotonic()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_update
        self.last_update = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

    def consume(self, amount: float = 1.0) -> float:
        """
        Consumes `amount` tokens if available.
        Returns:
            0.0 if tokens were consumed successfully.
            seconds (float) to wait before the tokens become available.
        """
        with self.lock:
            self._refill()
            if self.tokens >= amount:
                self.tokens -= amount
                return 0.0
            else:
                needed = amount - self.tokens
                return needed / self.refill_rate

# Configure default rate limits for Tavily search keyless tier:
# Default to 20 Requests Per Minute (refill = 20/60 = 0.33 requests/sec) with a burst capacity of 5.
TAVILY_LIMIT_RPM = float(os.environ.get("TAVILY_LIMIT_RPM", "20.0"))
TAVILY_LIMIT_BURST = float(os.environ.get("TAVILY_LIMIT_BURST", "5.0"))

tavily_rate_limiter = TokenBucket(
    capacity=TAVILY_LIMIT_BURST,
    refill_rate=TAVILY_LIMIT_RPM / 60.0
)
