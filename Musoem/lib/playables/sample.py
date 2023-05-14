import random, copy
from FoxDot import FileSynthDef, Buffer, PxRand, PRand, Pattern, PGroup, Clock, Player

from .playable import SoundObject
from ..player.section_player import SectionPlayer
from ..util.utils import R


class Sample(SoundObject):

    def __init__(self, instrument, keyword, bufnum):
        super().__init__(instrument, keyword)
        self.buf = bufnum
        #default_params = [1, 1, 4, 5, 1.1, 0, 0, 0.5, 0.5, 0.2, 10, 1, 1, 0] # change these to be plain playback, or remove them actually

    def copy(self):
        res = self.__class__(self.instrument, self.keyword, self.buf)
        res.params = self.params
        return res


    def __str__(self):
        return self.keyword + " bufnum " + str(self.buf)

    @property
    def total_dur(self):
        if isinstance(self.params["dur"], Pattern):
            return max(self.params["dur"])
        else:
            return self.params["dur"]


class SampleList(Sample):

    def __init__(self, instrument, keyword, bufnums):
        super().__init__(instrument, keyword, bufnums[0])
        self.__dict__["bufnums"] = bufnums #TODO: rename this variable
        self.__dict__["bufs"] = bufnums
        self.__dict__["ordered"] = False
        self.__dict__["buf_counter"] = -1

# TODO: refactor this to look prettier
    def initilize(self):
        if len(self.bufs) > 1:
            print("setting the random buffers")
            self.buf = R(10, self.bufs[0], self.bufs[-1], 1)
        else:
            self.buf = self.bufs[0]

    def copy(self):
        res = self.__class__(self.instrument, self.keyword , self.bufs)
        res.params = copy.deepcopy(self.params)
        res.ordered = self.ordered
        self.buf_counter += 1
        if self.buf_counter >= len(self.bufnums):
            self.buf_counter = 0
        res.buf_counter = self.buf_counter
        res.initilize()
        return res

    def play(self):
        if self.ordered:
            self.buf = self.bufnums[self.buf_counter]

        super().play()
