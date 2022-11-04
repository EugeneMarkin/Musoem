from music21.dynamics import Dynamic
from FoxDot import PRange, Pattern
from section import Section
from playable import PlayableGroup, ControlOperation
from now_playing import NowPlaying

# A class for music transformation

# When subclassing
# override pattern_keys() and return affected keys
# and override the "execute()" method

class SectionOperation:

    def __init__(self, keyword):
        self.keyword = keyword

    def pattern_keys(self):
        print("override me")
        return None

    def apply_to(self, playable):
        if isinstance(playable, PlayableGroup):
            # apply to each playable in group
            for p in playable: self.copy().apply_to(p)
            return
        elif isinstance(playable, ControlOperation):
            # operations can't be applied to control, so we look for sections
            if playable._parent is not None:
                self.apply_to(playable._parent)

        else: # Section
            self.section = playable
            if self.keyword in self.section.operations:
                return
            # section needs to know its operations so we can remove them
            self.section.operations[self.keyword] = self
            # store the initial values so that we can
            vals = [self.section[key].copy() for key in self.pattern_keys()]
            self.initial_vals = dict(zip(self.pattern_keys(), vals))

            self.execute()
            NowPlaying.update()

    def copy(self):
        return self.__class__(self.keyword)


    def reset(self):
        # undo the effect of the operation
        # if there were several operations, remove them from right to left
        # to return to the initial state.
        print("calling reset")
        for key in self.initial_vals.keys():
            print ("key ", key, "current ", self.section[key], "initial ", self.initial_vals[key])
            self.section[key] = self.initial_vals[key]

        # if we reset an operation, all the operations added later will be
        # effectively reset, so we remove them also
        ops = list(self.section.operations.keys())
        for i in range(ops.index(self.keyword), len(ops)):
            kw = ops[i]
            self.section.operations.pop(kw)
        self.section = None # TODO: add this back

    def __invert__(self):
        self.reset()
        NowPlaying.update()

    def __add__(self, other):
        return SectionOperationGroup(self, other)

    @property
    def display_style(self):
        return "italic"

class SectionOperationGroup(SectionOperation):

    def __init__(self, operations):
        self.keyword = super().__init__(reduce(lambda a,b: a.keyword + "," + b.keyword, operations))
        self.operations = operations


    def apply_to(self, section):
        for op in self.operations:
            op.apply_to(section)

    def append(self, other):
        if isinstance(other, SectionOperationGroup):
            for op in other.operations: self.append(op)
        else:
            self.operations.append(other)
            self.keyword += "," + other.keyword

    def __add__(self, other):
        if other in self.operations:
            other = other.copy()
        self.append(other)
        return self

class ReversePitch(SectionOperation):

    def pattern_keys(self):
        return ["degree", "oct"]

    def execute(self):
        self.section.degree = self.section.degree.reverse()
        self.section.oct = self.section.oct.reverse()

class Retrograde(SectionOperation):

    def pattern_keys(self):
        return ["dur"]

    def execute(self):
        self.section.dur = self.section.dur.reverse()


class TransposeOperation(SectionOperation):

    def __init__(self):
        super().init(["degree", "dur"])

    def execute(self):
        self.section.degree.reverse()
        self.section.dur.reverse()

class ReverseDurations(SectionOperation):

    def execute(self):
        self.section.dur.reverse()

class Crescendo(SectionOperation):

    def __init__(self, fromval = "pp", toval = "fff"):
        self.fromval = Dynamic(fromval).volumeScalar
        self.toval = Dynamic(toval).volumeScalar

    def amp_pattern(self):
        length = len(self.initialDegree)
        new_amp = Pattern([])
        for i in range(0, length):
            new_amp.append(self.fromval + (self.toval - self.fromval)/i)
        return new_amp

    def apply(self):
        section.player.amp = self.amp_pattern()

    def stop(self, section):
        print("stopping crescendo")
        self.player.amp = self.initialAmp

class Diminuendo(Crescendo):

    def __init__(self, fromval = "fff", toval = "pp"):
        super().__init__(toval, fromval)

    def amp_pattern(self):
        return super().amp_pattern().reverse()
