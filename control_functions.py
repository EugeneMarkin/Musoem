from music21.dynamics import Dynamic
from control import MasterTempo, MasterVolume

# TODO: this should be Control, and the current Control should be MidiControl
# a subclass of this guy

class ControlFunction:

    def __init__(self, control, arg, dur):
        self.control = control
        self.dur = duration
        self.arg = arg

    def start(self):
        print("start")
        self.control(arg, dur)

    def stop(self):
        print("stop")
        self.control.stop()

    def __call__(self):
        self.start()

class Crescendo(ControlFunction):

    def __init__(self, from_val , to_val, dur):
        self.from_val = Dynamic(fromval).volumeScalar
        self.to_val = Dynamic(toval).volumeScalar
        super().init(MasterVolume, to_val, dur)

class TempoChange(ControlFunction):

    def __init__(self, to_val, dur):


crescendo = Crescendo("ppp", "fff", 8)
diminuendo = Crescendo("fff", "ppp", 8)
