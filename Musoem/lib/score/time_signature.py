# A class representing time signature
from music21.meter.base import TimeSignature as M21TS

class TimeSignature:

    def __init__(self, num, dur):
        self.values = (num, dur)

    @classmethod
    def newFromM21TS(cls, ts: M21TS):
        num = int(ts.beatCount)
        dur = int(4 * float(ts.beatDuration.quarterLength))
        return TimeSignature(num, dur)

    @classmethod
    def none(cls):
        self.values = None

    def asTuple(self):
        return self.values

    def asString(self):
        if self.values is not None:
            return str(self.numerator) + " / " +  str(self.denominator)
        else:
            return "None"
    @property
    def numerator(self):
        return self.values[0]
    @property
    def denominator(self):
        return self.values[1]
