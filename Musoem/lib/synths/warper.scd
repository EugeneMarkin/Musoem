(
SynthDef(\warper, {arg buf = 0, overlaps = 4, start_time = 0, stretch = 1, harm = 1, windowsize = 6, amp = 1, pan = 0, attack = 10, decay = 1, sus = 1, release = 1, lfo = 0.5, cutoff = 400;
	var sig, env, lfos;
	sig = WarpOverlap.ar(2, buf, starttime: start_time, stretch: stretch, harm: harm, windowsize: windowsize)*amp;
	env = EnvGen.ar(Env.adsr(attack, decay, sus, release), doneAction:Done.freeSelf);
	lfos = LFTri.ar(lfo, 0, 0.5, 0.5);
	sig = env*sig*lfos;
	sig = Klank.ar(`[[800, 1200, 1100, 400], nil, [0.2, 0.2, 0.2, 0.2]], sig);
	sig = NHHall.ar(sig)*0.7;
	sig = Pan2.ar(Mix.ar(sig), pan);
	sig = sig * 0.9 + LFNoise0.ar(400, 0.1)*0.1;
		sig = BLowPass4.ar(sig, cutoff);
	Out.ar(4, sig);
}).add;
)


c = Buffer.readChannel(s, Platform.userHomeDir +/+ "Documents/Musoem_projects/survival kit/warper/1.wav", channels: [0,1])
Synth(\warper, [\buf: c, \pan: 0, \harm: 1, \lfo: 0.05]);
Synth(\warper, [\buf: c, \pan: -1, \harm: 5, \lfo: 0.3, \cutoff, 400, \amp, 0.5]);
Synth(\warper, [\buf: c, \pan: 1, \harm: 7, \lfo: 0.25, \cutoff, 400, \amp, 0.5]);
Synth(\warper, [\buf: c, \pan: 0.25, \harm: 6, \lfo: 0.15, \cutoff, 700]);
Synth(\warper, [\buf: c, \pan: -0.25, \harm: 6, \lfo: 0.15, \cutoff, 700]);
Synth(\warper, [\buf: c, \pan: 0, \harm: 3, \lfo: 0.05, \amp, 0.4]);

// try to add this after the "fruit" section, should be cool transition to whatever is next (prob. short gestures)
// maybe end this section abruptly, like with a very short release
