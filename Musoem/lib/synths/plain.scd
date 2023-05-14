SynthDef.new(\plain, {|bus = 0, buf = 0 ,dur = 5, enhance = 0, msmooth = 0.1, teeth = 0, comb = 0.5,
	                     lfohz = 0.5, lfodepth = 0.2, amp = 0.8,
	                     vibRate = 0.001, vibDepth = 0.001,
	                     vattack = 1, vdecay = 1, vrelease = 5, pan = 0, ypan = 1,  freeze = 1.1, rate = 1|
	var in, chain, output,fenv, volenv, envdur, timespan;
	timespan = vattack + vdecay + dur + vrelease;
	in = PlayBuf.ar(numChannels: 2, bufnum: buf, rate: rate * SinOsc.ar(vibRate,0, vibDepth, 1 - vibDepth)  , trigger: 1, startPos: 0, loop: 1);
    output = in * SinOsc.kr(lfohz, mul: lfodepth, add: 1 - lfodepth); // lfo
	volenv = EnvGen.ar(Env.new(levels:[0, amp, amp, amp, 0], times: [vattack, vdecay, dur, vrelease]), Line.kr(1, 0, timespan), doneAction: Done.freeSelf);
    output = Mix.new(output);
    output = Pan4.ar(volenv * output,xpos: pan, ypos: ypan);
	Out.ar(2, output);
}).add;

