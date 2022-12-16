from playable import Playable
from section_player import SectionPlayer
from FoxDot import FileSynthDef, Buffer, PxRand, Pattern, Clock, Player
import random

Clock.bpm = 60

param_keys = ["attack", "decay", "dur", "release", "freeze", "enhance", "teeth", "comb", "lfohz", "lfodepth", "pan", "rate", "vibRate", "vibDepth"]

# TODO: rename this to "Sampler"
class Sample(Playable):

    def __init__(self, keyword, instrument_key, bufnum):
        super().__init__(keyword)
        print("init sample keyword: ", keyword, "instrument: ", instrument_key, "bufnum: ", bufnum)
        self.bpm = [60]
        self.counter = 0
        self.instrument_key = instrument_key
        self.bufnum = bufnum
        self.keyword = keyword
        self.player = SectionPlayer()
        self.instrument = FileSynthDef(instrument_key)
        self.instrument.add()
        default_params = [1, 1, 4, 2, 1.1, 0, 0, 0.5, 0.5, 0.2, 0, 1, 1, 0]
        self.params = dict(zip(param_keys, default_params))


    def play(self):
        print("calling play sample, dur", self.params["dur"])
        if super().play() is None:
            return self
        self.player = SectionPlayer()
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
                                       pan = random.uniform(-0.5, 0.5),
                                       vibRate = self.params["vibRate"],
                                       vibDepth = self.params["vibDepth"])
        self.counter += 1

    def stop(self):
        if self._isplaying:
            self.player.stop()
        super().stop()

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if attr in param_keys:
            print("is in param keys ", attr, "val", value)
            self.params[attr] = value
            print("self.params[attr] is ", self.params[attr])


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
        print("initializing sample list with ", bufnums)
        super().__init__(keyword, instrument_key, bufnums[0])
        self.bufnums = bufnums
        self.bufnum = PxRand(bufnums[0], bufnums[-1])

    def copy(self):
        res = self.__class__(self.keyword, self.instrument_key, self.bufnums)
        res.params = self.params
        return res
