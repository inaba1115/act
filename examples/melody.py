from __future__ import annotations

import numpy as np
import random

import mido
from pythonosc.udp_client import SimpleUDPClient

from act.bpm import BPM
from act.mode import Mode
from act.note import Note
from act.osc_midi_bridge_client import OscMidiBridgeClient
from act.sched_midi import SchedMidi
from act.temporal_context import TemporalContext


def by_sched_midi(bpm: BPM, melody: list[tuple[Note, float]]) -> None:
    ports = mido.get_output_names()  # type: ignore
    port = mido.open_output(ports[0])  # type: ignore
    piano_client = SchedMidi(port, 0)

    t = 0
    for note, sus in melody:
        piano_client.enter(note, 64, sus, t)
        t += sus
    piano_client.run()


def by_osc_midi_bridge_client(bpm: BPM, melody: list[tuple[Note, float]]) -> None:
    udp_client = SimpleUDPClient("127.0.0.1", 57120)
    piano_client = OscMidiBridgeClient(udp_client, 0)

    tctx = TemporalContext()
    for note, sus in melody:
        piano_client.send_midi(note.midi_number, 64, sus, tctx.now())
        tctx.sleep(sus)


def main():
    bpm = BPM(130)
    mode = Mode.parse("A Minor")
    notes = mode.nth_notes(3, [random.randint(0, 10) for _ in range(16)])
    suss = np.array([random.randint(1, 8) for _ in range(16)]) * bpm.div(16)
    melody = list(zip(notes, suss))
    by_sched_midi(bpm, melody)
    by_osc_midi_bridge_client(bpm, melody)


if __name__ == "__main__":
    main()
