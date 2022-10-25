from section import SectionStub
from operations import *
from score import Score, MidiScore


class CommandMap:
    def __init__(self, score):
        self._load_score(score)
        self.operations = {}
        self.control = {}

    def _load_score(self, score):
        if isinstance(score, MidiScore):
            self.score = score.sections
        elif isinstance(score, Score):
            print("not implemented")

# brian eno oblique strategies
