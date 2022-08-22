#from score import Score
#from stream_parser import ScoreParser
from music21.stream.base import Score as M21Score
from music21.stream.base import Measure as M21Measure
from music21.stream.base import Voice as M21Voice
from music21 import converter
from score import Score
from parsers import ScoreParser
import sys


file_path = "~/Documents/Gymnopédie_No._1-3.musicxml"
test_path = "~/Documents/scoredot_test.musicxml"
tf_path = "~/Documents/tf_draft.musicxml"

m21_score = parse_musicxml_file(tf_path)

def parse_musicxml_file(path) -> M21Score:
    return converter.parse(path, format = "musicxml")

for part in m21_score.parts:
    print(part.id)

def test():
    print(file_path)
    m21_score = parse_musicxml_file(file_path)
    #score_parser = ScoreParser(m21_score)
    for part in m21_score.parts:
        for obj in part:
            if isinstance(obj, M21Measure):
                if obj.hasVoices():
                    print("has voices")
                    for some in obj.iter:
                        print(some)
                        if isinstance(some, M21Voice):
                            for o in some.notesAndRests:
                                print(o)


def test2():
    m21_score = parse_musicxml_file(test_path)
    score_parser = ScoreParser(m21_score)
    parts = score_parser.parts
    for part_key in parts:
        print(part_key)
        part = parts[part_key]
        for measure in part.measures:
            print("-------------------", measure.id)
            for voice in measure.voices.values():
                print('pitch', voice.pitch)
                print('octave', voice.octave)
                print('duration', voice.duration)
                print('bpm', voice.bpm)


def test3():
    m21_score = parse_musicxml_file(test_path)
    score = Score(m21_score)
    print(score.parts)
    for part_key in score.parts:
        print(part_key)
        part = score.parts[part_key]
        for voice_id in part.voices:
            print(voice_id)
            voice = part.voices[voice_id]
            for measure in voice.measures:
                print(measure.description)
def test4():
    m21_score = parse_musicxml_file(tf_path)
    score = Score(m21_score)
    print(score.parts)
    for part_key in score.parts:
        print(part_key)
        part = score.parts[part_key]
        for voice_id in part.voices:
            print(voice_id)
            voice = part.voices[voice_id]
            for measure in voice.measures:
                print(measure.description)

#test4()
print(type(sys.path))
for path in sys.path:
    print(path)

sys.path.append("/Users/eugenemarkin/Projects/scoredot")

test2()
