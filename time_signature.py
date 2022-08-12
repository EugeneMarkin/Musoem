# A class representing time signature

class TimeSignature:

    def __init__(self, num, dur):
        self.values = (num, dur)

    @classmethod
    def newFromM21TS(cls, ts: M21TS):
        num = int(ts.beatCount)
        dur = int(4 * float(ts.beatDuration.quarterLength))
        return TimeSignature(num, dur)

    def asTuple(self):
        return self.values

    def numerator(self):
        return self.values[0]

    def denominator(self):
        return self.values[1]
