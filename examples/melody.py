from __future__ import annotations

import random

import numpy as np

from act.bpm import BPM
from act.mode import Mode
from act.midi_over_osc import MidiOverOscClient
from act.temporal_context import TemporalContext


def main():
    piano_client = MidiOverOscClient("127.0.0.1", 33333)

    bpm = BPM(130)
    mode = Mode.parse("A Minor")

    notes = mode.nth_notes(3, [random.randint(0, 10) for _ in range(16)])
    durs = np.array([random.randint(1, 8) for _ in range(16)]) * bpm.div(16)
    melody = list(zip(notes, durs))

    tctx = TemporalContext()
    for note, dur in melody:
        piano_client.send_midi(note.midi_number, 64, dur, tctx.now())
        tctx.sleep(dur)


if __name__ == "__main__":
    main()
