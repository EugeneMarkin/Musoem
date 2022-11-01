from section import SectionStub
from operations import *
from score import Score, MidiScore
from control_operations import Crescendo


class CommandMap:
    def __init__(self, score):
        self.score = {}
        self._load_score(score)
        self.operations = {}
        self.wait_mark = ";"
        self.control = {"!" : Crescendo.new("!",dur = 5, fromval = "ppp", toval = "fff"),
                        "?" : Crescendo.new("?", dur = 5, fromval = "fff", toval = "ppp")}
        self.andKeywords = ["and", "And"]
        self.orKeywords = ["or", "Or"]
        self.pause_time = 2 # in beats

    def _load_score(self, score):
        if isinstance(score, MidiScore):
            self.score = score.sections
        elif isinstance(score, Score):
            print("not implemented")

    def add_control(self, list):
        for item in list:
            self.control[item.keyword] = item

    def add_operations(self, list):
        for item in list:
            self.operations[item.keyword] = item

    def __str__(self):
        res = "score: " + str(self.score)
        res += "\n control: " + str(self.control)
        res += "\n operations: " + str(self.operations)

        return res
