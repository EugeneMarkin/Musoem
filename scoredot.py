from music21 import converter
from music21.stream import Score as M21Score
from measure import Measure
from score import Score
import os

file_path = "~/Documents/Gymnopédie_No._1-3.musicxml"

# Parse MusicXML file into the music21 Score
def parse_musicxml_file(path) -> Score:
    return converter.parse(file_path, format = "musicxml")


def test():
    m21_score = parse_musicxml_file(file_path)
    for el in m21_score.elements:
        print(el)
    print(m21_score.metronomeMarkBoundaries())
    score = Score(m21_score)
    return score

score = test()
for voice in score.voices:
    print(voice)
    for measure in voice.measures:
        print(measure.description)

#get_measures(score, 0)
