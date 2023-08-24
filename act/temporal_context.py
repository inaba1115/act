from __future__ import annotations

import time


class TemporalContext:
    def __init__(self, delay: float = 0.02) -> None:
        self._vtime = time.time()
        self._delay = delay

    def now(self) -> float:
        return self._vtime + self._delay

    def sleep(self, sec: float) -> None:
        self._vtime += sec
        delta = self._vtime - time.time()
        if delta > 0:
            time.sleep(delta)
