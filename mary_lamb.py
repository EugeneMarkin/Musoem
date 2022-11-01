#sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from command_map import CommandMap
from score import MidiScore
from operations import ReversePitch
from control_operations import Crescendo

score = MidiScore("/Users/eugenemarkin/Music/Midi/Mary_score",bpm = 120)
mary_map = CommandMap(score)
mary_map.add_control([Crescendo.new("Rise", dur = 5, fromval = 'ppp', toval = 'fff')])
mary_map.add_operations([ReversePitch("reverse")])

#for key in mary_map.score.keys():
#    print(key)
#    section = mary_map.score[key]
#    print(section.description)
