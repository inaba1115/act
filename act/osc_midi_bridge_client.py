from __future__ import annotations

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder


class OscMidiBridgeClient:
    def __init__(self, client: udp_client.SimpleUDPClient, chan: int) -> None:
        self._client = client
        self._chan = chan

    def send_midi(self, note: int, velo: int, sus: float, ts: float) -> None:
        bundle = osc_bundle_builder.OscBundleBuilder(ts)  # type: ignore
        msg = osc_message_builder.OscMessageBuilder(address="/midi")
        msg.add_arg(note)
        msg.add_arg(velo)
        msg.add_arg(sus - 0.05)
        msg.add_arg(self._chan)
        bundle.add_content(msg.build())  # type: ignore
        self._client.send(bundle.build())
