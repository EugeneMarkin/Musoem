#sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from command_map import CommandMap
from score import FileScore
from operations import ReversePitch, Retrograde, Transpose
from control_operations import crescendo, reverb

score = FileScore("/Users/eugenemarkin/Music/Midi/drum_score",bpm = 100)
drum_map = CommandMap(score)
drum_map.add_control([crescendo("rise", fromval = 'pp', toval = 'fff', dur = 5),
                      reverb("space",0.1, 1, 5), reverb("land", 1, 0.1, 2)])

drum_map.add_operations([ReversePitch("opposite"),
                         Retrograde("backwards"),
                         Transpose("elevate", 12),
                         Transpose("down", -12)])
