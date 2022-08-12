import sys
sys.path.append("~/Projects/scoredot")

from music21 import converter
from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from measure import Measure
from score import Score
import os

file_path = "~/Documents/Gymnopédie_No._1-3.musicxml"
# Parse MusicXML file into the music21 Score
def parse_musicxml_file(path) -> Score:
    return converter.parse(file_path, format = "musicxml")
def test():
    m21_score = parse_musicxml_file(file_path)
    score = Score(m21_score)
    return score

score = test()

for key in score.all:
    print(key)

section1 = score.all["Piano_treble voice: -1"]
section2 = score.all["Piano_bass voice: 5"]
section3 = score.all["Piano_bass voice: 6"]

Clock.set_time(-1);
Scale.default.set(Tuning.ET12)
Root.defaul = 'C'
Clock.meter = (3, 4)
scale = Scale.chromatic
v1 >> keys(section1.pitch,
            dur = section1.duration,
            oct = section1.octave+2,
            bpm = section1.bpm,
            scale = scale)
v2 >> keys(section2.pitch,
            dur = section2.duration,
            oct = section2.octave+2,
            bpm = section2.bpm,
            scale = scale)
v3 >> keys(section3.pitch,
            dur = section3.duration,
            oct = section3.octave+2,
            bpm = section3.bpm,
            scale = scale)

sub_section = score.section(5, 7, "Piano", -1, "treble")

v4 >> pluck(sub_section.pitch,
            dur = sub_section.duration,
            oct = sub_section.octave,
            bpm = sub_section.bpm,
            scale = scale
            ).every(4, "stutter", 3
            ).every(2, "reverse", cycle=2
            ).every(3, "mirror")
#v4.stop()

p1 >> play("xoxo[*0]-**-xo", bpm=50)

p1.stop()
print(sub_section)

#get_measures(score, 0)
