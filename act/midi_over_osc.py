from __future__ import annotations

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder


class MidiOverOscClient:
    def __init__(self, address: str, port: int, chan: int = 0) -> None:
        self._client = udp_client.SimpleUDPClient(address, port)
        self._chan = chan

    def send_midi(self, note: int, velo: int, dur: float, ts: float) -> None:
        bundle = osc_bundle_builder.OscBundleBuilder(ts)  # type: ignore
        msg = osc_message_builder.OscMessageBuilder(address="/midi")
        msg.add_arg(note)
        msg.add_arg(velo)
        msg.add_arg(dur - 0.05)
        msg.add_arg(self._chan)
        bundle.add_content(msg.build())  # type: ignore
        self._client.send(bundle.build())
