from section import Section, SectionGroup
from music21.dynamics import Dynamic
from FoxDot import PRange, Pattern

# A class for music transformation
class Operation:

    def __init__(self, keyword):
        self.keyword = keyword

    def copy(self):
        return self.__class__(self.keyword)

    def reset(self):
        print("reset")

# A transformation that is applied to section of the score
class SectionOperation(Operation):

    def start(self, section):
        self.initialDegree = section.degree.copy()
        self.initialDur = section.dur.copy()
        self.initialOct = section.oct.copy()
        self.initialAmp = section.amp.copy()
        self.initialSus = section.sus.copy()
        self.initialBpm = section.bpm.copy()


# A transformation that is applied to sound regardless of the playing pattern(section)
class ControlOperation(Operation):


    def start(self):
        print("stub")

    def stop(self):
        print("stop control operation")

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

    def start(self, section):
        super().start(section)
        section.player.amp = self.amp_pattern()
        print("starting crescendo")

    def stop(self, section):
        print("stopping crescendo")
        self.player.amp = self.initialAmp

class Diminuendo(Crescendo):

    def __init__(self, fromval = "fff", toval = "pp"):
        super().__init__(toval, fromval)

    def amp_pattern(self):
        return super().amp_pattern().reverse()
