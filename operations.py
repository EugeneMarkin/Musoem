from music21.dynamics import Dynamic
from FoxDot import PRange, Pattern
from section import Section
from playable import PlayableGroup, ControlOperation

# A class for music transformation
class SectionOperation:

    def __init__(self, keyword):
        self.keyword = keyword

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
            # section needs to know its operations so we can remove them
            self.section.operations[self.keyword] = self
            # store the initial values so that we can
            self.initial_vals = list(map(lambda x: x.copy(), self.section.patterns))

            self.execute()

    def copy(self):
        return self.__class__(self.keyword)

        ## TODO: fix this
    def reset(self):
        # undo the effect of the operation
        # if there were several operations, remove them from right to left
        # to return to the initial state.
        print("calling reset")
        for i in range(0, len(self.initial_vals)):
            self.section.patterns[i] = self.initial_vals[i]
        ops = list(self.section.operations.keys())
        # if we reset an operation, all the operations added later will be
        # effectively reset, so we remove them also
        for i in range(ops.index(self.keyword), len(ops)):
            kw = ops[i]
            self.section.operations.pop(kw)
        # self.section = None # TODO: add this back

class SectionOperationGroup(SectionOperation):

    def __init__(self, operations):
        self.operations = operations

    def apply_to(self, section):
        for op in self.operations:
            op.apply_to(section)

class ReversePitch(SectionOperation):

    # TODO: figure out how to update player in superclass

    def execute(self):
        self.section.degree = self.section.degree.reverse()
        self.section.player.degree = self.section.degree
        self.section.oct = self.section.oct.reverse()
        self.section.player.oct = self.section.oct

    def reset(self):
        super().reset()
        self.section.degree = self.initial_vals[0]
        self.section.player.degree = self.section.degree
        self.section = None

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
