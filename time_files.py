# initial setup for scoredot to run with FoxDot
sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from score import Score
from music21.stream.base import Score as M21Score
from music21 import converter
# score file path
fp = "~/Documents/time_files_full.musicxml"
# load the score into musc21
m21_score = converter.parse(fp, format = "musicxml")
# parse the score
score = Score(m21_score)
# this gives the parts in the score
print(score.parts.keys())
#   Bass Synth Parts
# get first pattern from the score: measures 1 to 7

# sine sub
sine_sub = score.parts["Sine Sub"]
print(sine_sub)
for v in sine_sub.voices:
    voice = sine_sub.voices[v]
    for m in voice.measures:
        print(m, m.index, m.degree, m.dur, m.sus)

170 181

ssp2 = score.section(170, 181, "Sine Sub")

ssp2.add_midi_out(3)

ssp2.play()


# START THE PIECE
Clock.set_time(-1)
bass.play()
bass.lfoRate = 0.5
bass.lfoDepth = 0.8
bass.room = 1
bass.mix = 1
bass.jitter = 0

bass.lfoRate = 0.1

b.jitter = 0.1

mid.play()

mid.lfoRate = P[0.3, 0.5, 0.7]
mid.amp = 1.4

mid.degree = P[0.5, 0 ,6, 0, 0.5, 0, 0, 0, 2, 1, 1, 1]

hi.play()
hi.room = 1
hi.mix = 1

hi.attack = 1
hi.lfoRate = 0.5

hi.jitter = 0.2


hi.degree = hi.degree + P[0.125, 0.25]

low.play()

low.

m1 >> MidiOut(degree = P[1, 2, 3], blur = P[1,2])

p1 >> nylon(P[1,2,3])

mymidi = SynthDef("mymidi")

p2 >> mymidi(P[1, 2, 3])

p1 >> stretch("KSHMR_Vocal_Texture_07_G", dur = 10, pitch = 2)

voc = FileSynthDef("erepitchsampler")
voc.add()

p1 >> voc(P[0,1,2], dur = P[2,2, 2], buf = 100, scale = Scale.chromatic)

fbadd = FileSynthDef("efbadd")
fbadd.add()

p2 >> fbadd(P[1, 2, 3], fb = 0.01, amp = 1, attack = 0.5, comb = 0.03)
