from __future__ import annotations

import sched
import time
import typing

import mido

from act.note import Note


def note_on(port: typing.Any, chan: int, note: Note, velo: int):
    msg = mido.Message("note_on", channel=chan, note=note.midi_number, velocity=velo)
    port.send(msg)


def note_off(port: typing.Any, chan: int, note: Note):
    msg = mido.Message("note_off", channel=chan, note=note.midi_number)
    port.send(msg)


class SchedMidi:
    def __init__(self, port: typing.Any, chan: int) -> None:
        self._s = sched.scheduler(time.monotonic, time.sleep)
        self._port = port
        self._chan = chan

    def enter(self, note: Note, velo: int, sus: float, delay: float) -> None:
        self._s.enter(delay, 1, note_on, argument=(self._port, self._chan, note, velo))
        self._s.enter(delay + sus, 1, note_off, argument=(self._port, self._chan, note))

    def run(self) -> None:
        self._s.run()
