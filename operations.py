from music21.dynamics import Dynamic
from FoxDot import PRange, Pattern
from section import Section
from playable import PlaybleGroup, ControlOperation

# A class for music transformation
class SectionOperation:

    def __init__(self, keyword):
        self.keyword = keyword

    def apply_to(self, playable):
        if isinstance(playable, PlayableGroup):
            # apply to each playable in group
            map(lambda p: self.copy().apply_to(p), playable)
        elif isinstance(playable, ControlOperation):
            # operations can't be applied to control, so we look for sections
            if playable._parent is not None:
                self.apply_to(playable._parent)
            elif playable._next is not None:
                self.apply_to(playable._next)
        else: # Section
            self.section = playable
            # section needs to know its operations so we can remove them
            self.secton.operations[self.keyword] = self
            # store the initial values so that we can
            self.initial_vals = list(map(lambda x: x.copy(), self.section.patterns))

    def copy(self):
        return self.__class__(self.keyword)

    def reset(self):
        # undo the effect of the operation
        # if there were several operations, remove them from right to left
        # to return to the initial state.
        for i in range(0, len(self.initial_vals)):
            self.section.patterns[i] = self.initial_vals[i]
        ops = list(self.section.operations.keys())
        # if we reset an operation, all the operations added later will be
        # effectively reset, so we remove them also
        for i in range(list(ops.index(self.keyword), len(ops)):
            kw = ops[i]
            self.section.operations.pop(kw)
        self.section = None

class SectionOperationGroup(SectionOperation):

    def __init__(self, operations):
        self.operations = operations

    def apply_to(self, section):
        for op in self.operations:
            op.apply_to(section)

class ReversePitch(SectionOperation):

    def apply_to(self, section):
        super().apply_to(section)
        self.section.degree.reverse()

class ReverseDurations(SectionOperation):

    def apply_to(self, section):
        super().apply_to(section)
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
