from ..score.measure import Measure
from FoxDot import Pattern, Player, FileSynthDef, Env, Scale, MidiOut, Clock, rest
from .playable import SoundObject
import random

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

class Section(SoundObject):

    def __init__(self, measures:[Measure], instrument, keyword = "None"):
        super().__init__(instrument, keyword)
        self.__dict__["_measures"] = measures
        keys = ["degree", "oct", "dur", "sus", "bpm", "amp"]
        for k in keys:
            self.params[k] = Pattern([])

        for mes in measures:
            self.params["degree"].extend(mes.degree)
            self.params["oct"].extend(mes.oct)
            self.params["dur"].extend(mes.dur)
            self.params["sus"].extend(mes.sus)
            self.params["bpm"].extend(mes.bpm)
            self.params["amp"].extend(mes.amp)

        self.params["scale"] = Scale.chromatic

        print("sound object: ", keyword)
        print(self.description)

    def copy(self):
        cp = self.__class__([], instrument = self.instrument, keyword = self.keyword)
        cp.__dict__["measures"] = self._measures.copy()
        cp.__dict__["params"] = self.params.copy()
        return cp

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
        return str(self.params)


class SectionList(Section):

    def __init__(self, instrument, keyword, list):
        super().__init__([], instrument, keyword)
        self.initialized = False
        self.list = list
        self.index = 0
        self.ordered = False
        self.initialized = True

    def copy(self):
        return self.__class__(self.list, self.keyword)

    def play(self):
        self.__dict__["params"] = self.next_section.params
        self.__dict__["instrument"] = self.next_section.intrument
        super().play()

    @property
    def next_section(self):
        if self.ordered:
            res = self.list[self.index]
            if self.index < len(self.list) - 1:
                self.index += 1
            else:
                self.index = 0
            return res
        else:
            idx = random.randint(0, len(self.list) - 1)
            return self.list[idx]

    def __iter__(self):
        return iter(self.list)
