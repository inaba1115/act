(
MIDIClient.init;
MIDIClient.destinations;
~midi = MIDIOut.new(0);
)

(
OSCdef(\midi, {|msg, time|
	var chan = msg[1];
	var note = msg[2];
	var velo = msg[3];
	var sus = msg[4];
	SystemClock.schedAbs(time, {
		~midi.noteOn(chan, note, velo);
	});
	SystemClock.schedAbs(time+sus, {
		~midi.noteOff(chan, note, velo);
	});
}, '/midi');
)
