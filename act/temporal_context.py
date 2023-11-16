from __future__ import annotations

import time
import copy


class TemporalContext:
    def __init__(self, delay: float = 1.0, assert_delta: float = 0.05) -> None:
        self._vtime = time.time()
        self._initial_vtime = self._vtime
        self._delay = delay
        self._assert_delta = assert_delta

    def init(self) -> None:
        self._vtime = time.time()
        self._initial_vtime = self._vtime

    def now(self) -> float:
        return self._vtime + self._delay

    def sleep(self, sec: float) -> None:
        self._vtime += sec
        delta = self._vtime - time.time()
        if delta > 0:
            time.sleep(delta)

    def seek(self, sec: float) -> None:
        self._vtime += sec

    def assert_vtime(self) -> None:
        if abs(self._vtime - time.time()) > self._assert_delta:
            raise

    def fork(self) -> TemporalContext:
        return copy.deepcopy(self)

    def get_vtime_rel(self) -> float:
        return self._vtime - self._initial_vtime
