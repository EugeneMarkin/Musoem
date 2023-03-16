import random
from FoxDot import FileSynthDef, Buffer, PxRand, Pattern, PGroup, Clock, Player

from .playable import SoundObject
from ..player.section_player import SectionPlayer


class Sample(SoundObject):

    def __init__(self, instrument, keyword, bufnum):
        super().__init__(instrument, keyword)
        self.bufnum = bufnum
        #default_params = [1, 1, 4, 5, 1.1, 0, 0, 0.5, 0.5, 0.2, 10, 1, 1, 0] # change these to be plain playback, or remove them actually

    def copy(self):
        res = self.__class__(self.instrument, self.keyword, self.bufnum)
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

    def __init__(self, instrument, keyword, bufnums):

        super().__init__(instrument, keyword, bufnums[0])
        self.__dict__["bufnums"] = bufnums
        if len(bufnums) > 1:
            self.bufnum = PxRand(bufnums[0], bufnums[-1])
        else:
            self.bufnum = bufnums[0]
        self.__dict__["ordered"] = False
        self.__dict__["buf_counter"] = -1

    def copy(self):
        res = self.__class__(self.instrument, self.keyword , self.bufnums)
        res.params = self.params
        res.ordered = self.ordered
        self.buf_counter += 1
        res.buf_counter = self.buf_counter
        return res

    def play(self):
        if self.ordered:
            self.bufnum = Pattern(self.bufnums)[self.buf_counter]

        super().play()
