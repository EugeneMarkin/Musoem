from measure import Measure
from FoxDot import Pattern

class Section:
    def __init__(self, measures:[Measure]):
        self.pitch = Pattern([])
        self.octave = Pattern([])
        self.duration = Pattern([])
        self.bpm = Pattern([])
        # TODO: implement this
        self.time_sig = Pattern([])

        for mes in measures:
            self.pitch.extend(mes.pitch)
            self.octave.extend(mes.octave)
            self.duration.extend(mes.duration)
            self.bpm.extend([mes.bpm]*len(mes.pitch))
    @property
    def description(self):
        res = "pitch: " + str(self.pitch) + ", "
        res += "ocatave: " + str(self.octave) + ", "
        res += "duration: " + str(self.duration) + ", "
        res += "bpm: " + str(self.bpm)
        return res
