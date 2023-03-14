from ..score.measure import Measure
from FoxDot import Pattern, Player, FileSynthDef, Env, Scale, MidiOut, Clock, rest, P
from .playable import SoundObject

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

class Section(SoundObject):

    def __init__(self, measures:[Measure], instrument, keyword = "None"):
        super().__init__(instrument, keyword)
        self.initialized = False
        self._measures = measures
        keys = ["degree", "oct", "dur", "sus", "bpm", "amp"]
        for k in keys:
            self.params[k] = P([])

        for mes in measures:
            self.params["degree"].extend(mes.degree)
            self.params["oct"].extend(mes.oct)
            self.params["dur"].extend(mes.dur)
            self.params["sus"].extend(mes.sus)
            self.params["bpm"].extend(mes.bpm)
            self.params["amp"].extend(mes.amp)

        self.initialized = True

    def copy(self):
        return self.__class__(self._measures, instrument = self.instrument, keyword = self.keyword)

    @property
    def total_dur(self):
        if self._times == None:
            return None
        res = 0
        for el in self.dur:
            if (isinstance(el, float) or isinstance(el, int)):
                res += el
            elif isinstance(el, rest):
                res += el.dur
        return res * self._times

    @property
    def loop(self):
        self * -1
        return self

    def __str__(self):
        return "Section " + self.keyword

    @property
    def description(self):
        return str(self.patterns)
