from measure import Measure
from FoxDot import Pattern

class Section:
    def __init__(self, measures:[Measure]):
        self.pitch = Pattern([])
        self.octave = Pattern([])
        self.duration = Pattern([])
        self.offset = Pattern([])
        for mes in measures:
            self.pitch.extend(mes.pitch)
            self.octave.extend(mes.octave)
            self.duration.extend(mes.duration)
            self.offset.extend(mes.offset)
