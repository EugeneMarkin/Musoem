from music21.dynamics import Dynamic
from ..playables.control import MidiControl

def crescendo(keyword, fromval, toval, dur):
    from_v = Dynamic(fromval).volumeScalar
    to_v = Dynamic(toval).volumeScalar
    return MidiControl(keyword, 17, from_v, to_v, dur)

def reverb(keyword, fromval, toval, dur):
    return MidiControl(keyword, 18, fromval, toval, dur)
