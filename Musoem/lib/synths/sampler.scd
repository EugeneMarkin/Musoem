SynthDef.new(\sampler, {|bus = 0, buf = 0 ,dur = 5, enhance = 0, msmooth = 0.1, teeth = 0, comb = 0.5,
	                     lfohz = 0.5, lfodepth = 0.2, amp = 0.8,
	                     vibRate = 0.001, vibDepth = 0.2,
	                     vattack = 1, vdecay = 1, vrelease = 5, pan = 0, freeze = 1.1, rate = 1|

	var in, chain, output, frames = 2**13, bw, fenv, volenv, envdur, timespan, freezetime;
	    timespan = vattack + vdecay + dur + vrelease;
	    in = PlayBuf.ar(numChannels: 2, bufnum: buf, rate: rate * SinOsc.ar(vibRate, 0, vibDepth, 1 - vibDepth)  , trigger: 1, startPos: 0, loop: 1);
        // raise the buffer size (no of frames), notice the delay.
        chain = FFT(LocalBuf(frames), in, 0.5, 0);
	    chain = PV_SpectralEnhance(chain, enhance, ratio:2, strength: 0.3);
        chain = PV_RectComb(chain,teeth, width: comb); //weird comb filter thingy
    	freezetime = (BufFrames.kr(buf)/(s.sampleRate))*freeze;

	    chain = PV_Freeze(chain, Line.kr(-1, 0.01, freezetime));

	    output = IFFT(chain);

    	output = output * SinOsc.kr(lfohz, mul: lfodepth, add: 1 - lfodepth); // lfo
	    volenv = EnvGen.ar(Env.new(levels:[0, 1, amp, amp, 0], times: [vattack, vdecay, dur, vrelease]), Line.kr(1, 0, timespan), doneAction: Done.freeSelf);
    	output = Mix.new(output);
     	output = Pan2.ar(volenv * output,pos: pan);

	ReplaceOut.ar(bus, output);
}).add;

