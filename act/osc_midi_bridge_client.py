from __future__ import annotations

from pythonosc import udp_client
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder
from act_playground import dev_temporal_context


class OscMidiBridgeClient:
    def __init__(
        self,
        tctx: dev_temporal_context.TemporalContext,
        client: udp_client.SimpleUDPClient,
        chan: int = 0,
    ) -> None:
        self._tctx = tctx
        self._client = client
        self._chan = chan

    def send_midi(self, note: int, velo: int, sus: float, ts: float = None) -> None:
        if ts is None:
            ts = self._tctx.now()
        bundle = osc_bundle_builder.OscBundleBuilder(ts)
        msg = osc_message_builder.OscMessageBuilder(address="/midi")
        msg.add_arg(self._chan)
        msg.add_arg(note)
        msg.add_arg(velo)
        msg.add_arg(sus)
        bundle.add_content(msg.build())
        self._client.send(bundle.build())
