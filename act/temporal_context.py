from __future__ import annotations

import copy
import time


class TemporalContext:
    def __init__(self, delay: float = 0.02) -> None:
        self.vtime = time.time()
        self.delay = delay

    def now(self) -> float:
        return self.vtime + self.delay

    def sleep(self, sec: float) -> None:
        self.vtime += sec
        delta = self.vtime - time.time()
        if delta > 0:
            time.sleep(delta)

    def reset(self) -> None:
        self.vtime = time.time()

    def clone(self) -> TemporalContext:
        return copy.deepcopy(self)
