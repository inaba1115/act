from __future__ import annotations

from pythonosc.udp_client import SimpleUDPClient

from act.bpm import BPM
from act.mode import Mode
from act.note import Note
from act.osc_midi_bridge_client import OscMidiBridgeClient
from act.temporal_context import TemporalContext
from act.tidal_tracker import TidalTracker


udp_client = SimpleUDPClient("127.0.0.1", 57120)
drums_client = OscMidiBridgeClient(udp_client, 0)
piano_client = OscMidiBridgeClient(udp_client, 1)


def bd_fn(ctx, *args):
    drums_client.send_midi(36, 100, ctx["dur"], ctx["ts"])


def sn_fn(ctx, *args):
    drums_client.send_midi(38, 100, ctx["dur"], ctx["ts"])


def hc_fn(ctx, *args):
    drums_client.send_midi(42, 100, ctx["dur"], ctx["ts"])


def ho_fn(ctx, *args):
    drums_client.send_midi(46, 100, ctx["dur"], ctx["ts"])


def p_fn(ctx, *args):
    notes = args[0].split(",")
    for note in notes:
        piano_client.send_midi(Note.parse(note).midi_number, 100, ctx["dur"], ctx["ts"])


def to_chord_str(notes: list[Note]) -> str:
    return ",".join([str(x) for x in notes])


tt = TidalTracker(
    {
        "bd": bd_fn,
        "sn": sn_fn,
        "hc": hc_fn,
        "ho": ho_fn,
        "p": p_fn,
    }
)


def main():
    tctx = TemporalContext()
    bpm = BPM(70)
    mode1 = Mode.parse("G Whole Tone")
    mode2 = Mode.parse("D Minor")
    mode3 = Mode.parse("E Minor")

    for i in range(6):
        pat = [
            "hc/2 [_@2 hc/2 ho/3]*2 hc/3 [hc/4 ho]",
            "[bd/2 _ _ bd] sn _ bd/3 [_ sn _ _ sn]*2",
            " ".join([f"p:{n}" for n in mode1.sample_notes(3, 0, 14, 11)]),
            "_ p:{}@2".format(to_chord_str(mode2.sample_notes(2, 0, 18, 3))),
        ]
        tt.run(tctx, pat, bpm.bar(), 1)

    for i in range(6):
        pat = [
            "hc/3 _ ho [hc ho] hc/4 [_ ho] hc",
            "sn sn/2 bd [sn _ sn] _ bd",
            " ".join([f"p:{n}" for n in mode1.sample_notes(3, 0, 14, 11)]),
            "_ p:{}@4".format(to_chord_str(mode3.sample_notes(2, 0, 18, 3))),
        ]
        tt.run(tctx, pat, bpm.bar(), 1)


if __name__ == "__main__":
    main()
