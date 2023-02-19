#sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from command_map import CommandMap
from score import FileScore
from operations import ReversePitch, Retrograde, Transpose
from control_operations import crescendo, reverb

score = FileScore("/Users/eugenemarkin/Music/Midi/Mary_score",bpm = 120)
mary_map = CommandMap(score)
mary_map.add_control([crescendo("rise", fromval = 'pp', toval = 'fff', dur = 5),
                      reverb("space",0.1, 1, 5), reverb("land", 1, 0.1, 2)])

mary_map.add_operations([ReversePitch("opposite"),
                         Retrograde("backwards"),
                         Transpose("elevate", 12),
                         Transpose("down", -12)])



#for key in mary_map.score.keys():
#    print(key)
#    section = mary_map.score[key]
#    print(section.description)
# Chambers Alvin Lucier
