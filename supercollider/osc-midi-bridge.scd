(
MIDIClient.init;
MIDIClient.destinations;
~midi = MIDIOut.new(0);
)

(
OSCdef(\midi, {|msg, time|
	var note = msg[1];
	var velo = msg[2];
	var sus = msg[3];
	var chan = msg[4];
	SystemClock.schedAbs(time, {
		~midi.noteOn(chan, note, velo);
	});
	SystemClock.schedAbs(time+sus, {
		~midi.noteOff(chan, note, velo);
	});
}, '/midi');
)
