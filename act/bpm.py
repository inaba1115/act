from __future__ import annotations


class BPM:
    def __init__(self, bpm: float) -> None:
        self._bpm = bpm
        self._sec_per_beat = 60 / bpm
        self._sec_per_bar = 60 / bpm * 4

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(bpm={self._bpm!r})"

    def __str__(self) -> str:
        return str(self._bpm)

    def bpm(self) -> float:
        return self._bpm

    def bar(self) -> float:
        return self._sec_per_bar

    def div(self, n: int) -> float:
        return self._sec_per_bar / n
