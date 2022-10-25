#sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from command_map import CommandMap
from score import MidiScore

score = MidiScore("/Users/eugenemarkin/Music/Midi/Mary_score",bpm = 120)
mary_map = CommandMap(score)

for key in mary_map.score.keys():
    print(key)
    section = mary_map.score[key]
    print(section.description)
