from music21.dynamics import Dynamic
from FoxDot import PRange, Pattern, PGroup

from ..base.entity import Entity
from ..playables.section import Section
from ..playables.sample import Sample
from ..playables.playable import SoundGroup
from ..playables.control import Control
from ..player.now_playing import NowPlaying

# A class for music transformation

class Operation(Entity):

    def copy(self):
        return self.__class__(self.keyword)

    def execute(self, sound_object):
        self.__dict__["sound"] = sound_object
        self.__dict__["initial_params"] = sound_object.params.copy()
        self.__dict__["changed_params"] = []
        self.perform()

    def perform(self):
        print("override me")

    def undo(self):
        if not self.sound:
            return
        for key in self.changed_params:
            self.sound.__setattr__(key, self.initial_params[key])
        NowPlaying.update()

    def __setattr__(self, key, value):
        if self.sound is not None and key in self.sound.params:
            self.changed_params.append(key)
            self.sound.__setattr__(key, value)
        else:
            self.__dict__[key] = value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif "sound" in self.__dict__ and key in self.__dict__["sound"].params:
            return self.__dict__["sound"][key]
        return None

    def __invert__(self):
        self.undo()

    def __add__(self, other):
        return OperationGroup(self, other)

class OperationGroup(Operation):

    def __init__(self, operations):
        self.keyword = super().__init__(reduce(lambda a,b: a.keyword + "," + b.keyword, operations))
        self.operations = operations

    def append(self, other):
        if isinstance(other, OperationGroup):
            for op in other.operations:
                if op not in self.operations:
                    self.append(op)
        else:
            self.operations.append(other)
            self.keyword += "," + other.keyword

    def __add__(self, other):
        if other in self.operations:
            return self
        self.append(other)
        return self


class ReversePitch(Operation):

    def perform(self):
        self.degree = self.degree.reverse()
        self.oct = self.oct.reverse()

class Retrograde(Operation):

    def perform(self):
        self.dur = self.dur.reverse()

# Transposes the sound by a number of semitones
class Transpose(Operation):

    def __init__(self, t):
        super().__init__()
        self.t = t

    def copy(self):
        return self.__class__(self.t, self.keyword)

    def perform(self):
        self.degree = self.degree + self.t

#TODO: refactor this
class Crescendo(Operation):

    def __init__(self, fromval = "pp", toval = "fff"):
        self.fromval = Dynamic(fromval).volumeScalar
        self.toval = Dynamic(toval).volumeScalar

    def copy(self):
        return self.__class__(fromval, toval)

    def amp_pattern(self):
        length = len(self.degree)
        new_amp = Pattern([])
        for i in range(0, length):
            new_amp.append(self.fromval + (self.toval - self.fromval)/i)
        return new_amp

    def perform(self):
        self.amp = self.amp_pattern()


class Diminuendo(Crescendo):

    def __init__(self, fromval = "fff", toval = "pp"):
        super().__init__(toval, fromval)

    def amp_pattern(self):
        return super().amp_pattern().reverse()


class Multiply(Operation):

    def __init__(self, value, pan):
        super().__init__()
        self.value = value
        if isinstance(pan, list):
            self.pan = pan
        else:
            self.pan = [pan]

    def copy(self):
        return self.__class__(value, pan)

    def execute(self):
        if isinstance(self.sound, Sample):
            if isinstance(self.bufnum, Pattern) and val <= len(self.bufnum):
                self.bufnum = PGroup([self.bufnum[i] for i in range(0, self.value)] )
            else:
                self.bufnum = PGroup([self.bufnum]*self.value)
        else:
            self.degree = PGroup([self.degree]*self.value)

        self.pan = PGroup(pan)
