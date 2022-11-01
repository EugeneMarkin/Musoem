from music21.dynamics import Dynamic
from control import MasterTempo, MasterVolume
from playable import ControlOperation

class Crescendo(ControlOperation):

    @classmethod
    def new(self, keyword, dur, fromval, toval):
        from_val = Dynamic(fromval).volumeScalar
        to_val = Dynamic(toval).volumeScalar
        return Crescendo(keyword, MasterVolume, dur, {"to_val" : to_val, "from_val" : to_val})

    def execute(self):
        print("executing control")

    def finish(self):
        print("finish control")

class TempoChange(ControlOperation):

    def __init__(self, to_val, dur):
        print("foo")
