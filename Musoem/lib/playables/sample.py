import random
from FoxDot import FileSynthDef, Buffer, PxRand, Pattern, PGroup, Clock, Player

from .playable import Playable
from ..player.section_player import SectionPlayer

Clock.bpm = 60

param_keys = ["attack", "decay", "dur", "release", "freeze", "enhance", "teeth", "comb", "lfohz", "lfodepth", "pan", "rate", "vibRate", "vibDepth"]

# TODO: rename this to "Sampler"
class Sample(Playable):

    def __init__(self, keyword, instrument_key, bufnum):
        super().__init__(keyword)
        self.bpm = [60]
        self.instrument_key = instrument_key
        self.bufnum = bufnum
        self.keyword = keyword
        self.player = SectionPlayer()
        self.instrument = FileSynthDef(instrument_key)
        self.instrument.add()
        default_params = [1, 1, 4, 5, 1.1, 0, 0, 0.5, 0.5, 0.2, 10, 1, 1, 0]
        self.params = dict(zip(param_keys, default_params))


    def play(self):
        if super().play() is None:
            return self
        self.player = SectionPlayer()
        if isinstance(self.bufnum, PGroup):
            # TODO: fix this
            panVal = PGroup([-0.89, 0, 0.89])
        else :
            panVal = PxRand(-self.params["pan"], self.params["pan"])/10

        self.player >> self.instrument(bpm = 60,
                                       buf = self.bufnum,
                                       amp = 0.4,
                                       dur = self.params["dur"],
                                       freeze = self.params["freeze"],
                                       enhance = self.params["enhance"],
                                       lfohz = self.params["lfohz"],
                                       lfodepth = self.params["lfodepth"],
                                       comb = self.params["comb"],
                                       teeth = self.params["teeth"],
                                       rate = self.params["rate"],
                                       pan = panVal,
                                       vibRate = self.params["vibRate"],
                                       vibDepth = self.params["vibDepth"],
                                       vattack = self.params["attack"],
                                       vrelease = self.params["release"],
                                       vdecay = self.params["decay"])


    def stop(self):
        if self._isplaying:
            self.player.stop()
        super().stop()

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if attr in param_keys:
            self.params[attr] = value


    def copy(self):
        res = self.__class__(self.keyword, self.instrument_key, self.bufnum)
        res.params = self.params
        return res

    def __str__(self):
        return self.keyword + " bufnum " + str(self.bufnum)

    @property
    def total_dur(self):
        if isinstance(self.params["dur"], Pattern):
            return max(self.params["dur"])
        else:
            return self.params["dur"]


class SampleList(Sample):


    def __init__(self, keyword, instrument_key, bufnums):

        super().__init__(keyword, instrument_key, bufnums[0])
        self.bufnums = bufnums
        self.bufnum = PxRand(bufnums[0], bufnums[-1])
        self.ordered = False
        self.buf_counter = -1

    def copy(self):
        res = self.__class__(self.keyword, self.instrument_key, self.bufnums)
        res.params = self.params
        res.ordered = self.ordered
        self.buf_counter += 1
        res.buf_counter = self.buf_counter
        return res

    def play(self):
        if self.ordered:
            self.bufnum = Pattern(self.bufnums)[self.buf_counter]
            print("bufnums: ", Pattern(self.bufnums))
            print("ORDERED bn: ", self.bufnum, " counter", self.buf_counter)

        super().play()
