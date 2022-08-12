from music21 import converter
from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from measure import Measure
from score import Score
import os

file_path = "~/Documents/fugue2.musicxml"
# Parse MusicXML file into the music21 Score
def parse_musicxml_file(path) -> M21Score:
    return converter.parse(file_path, format = "musicxml")

m21_full_score = parse_musicxml_file(file_path)
score = Score(m21_full_score)

print(score.all)

sop_sec = score.section(1, 33, "Solo Soprano", -1, "treble")
alto_sec = score.section(1, 33, "Solo Alto", -1, "treble")
tenor_sec = score.section(1, 33, "Solo Tenor", -1, "treble8vb")
bass_sec = score.section(1, 33, "Solo Bass", -1, "bass")


Scale.default.set(Tuning.ET12)
Root.default = 'C'
scale = Scale.chromatic

print(SynthDefs)
# soprano, prophet, klank, jbass

Clock.set_time(-1);
s1 >> sinepad(sop_sec.pitch,
              dur = sop_sec.duration,
              oct = sop_sec.octave + 1,
              bpm = sop_sec.bpm,
              scale = scale,
              sus = sop_sec.duration*2,
              amp = 0.6 )
a1 >> sinepad(alto_sec.pitch,
              dur = alto_sec.duration,
              oct = alto_sec.octave + 1,
              bpm = alto_sec.bpm,
              scale = scale,
              sus = alto_sec.duration * 2,
              amp = 0.7)
t1 >> klank(tenor_sec.pitch,
              dur = tenor_sec.duration,
              oct = tenor_sec.octave + 1,
              bpm = tenor_sec.bpm,
              scale = scale)
b1 >> jbass(bass_sec.pitch,
            dur = bass_sec.duration,
            oct = bass_sec.octave + 2,
            bpm = bass_sec.bpm,
            scale = scale,
            sus = 8,
            amp = 0.3)

te >> sinepad([1,2,3,4])
