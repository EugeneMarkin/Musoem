from section import SectionStub
from operations import *
from score import Score, FileScore, SectionList
from control_operations import crescendo


class CommandMap:
    def __init__(self, score, operations = {}):
        self.score = {}
        self._load_score(score)
        self.operations = operations
        self.wait_mark = ";"
        self.control = {"!" : crescendo("!",dur = 10, fromval = "ppp", toval = "fff"),
                        "?" : crescendo("?", dur = 10, fromval = "fff", toval = "ppp")}
        self.andKeywords = ["and", "And"]
        self.orKeywords = ["or", "Or"]
        self.pause_time = 2 # in beats

    def _load_score(self, score):
        if isinstance(score, FileScore):
            self.score = score.sections
        elif isinstance(score, Score):
            print("not implemented")

    def add_control(self, list):
        for item in list:
            self.control[item.keyword] = item

    def add_operations(self, list):
        for item in list:
            self.operations[item.keyword] = item

    def get_section(self, kw):
        return self._get_item(kw, self.score)

    def get_operation(self, kw):
        return self._get_item(kw, self.operations)

    def get_control(self, kw):
        return self._get_control(kw, self.control)

    def _get_item(self, kw, dict):
        obj = dict[kw]
        # TODO: make section list subclass of Section
        if isinstance(obj, SectionList):
            return obj.next
        else:
            return obj

    def __str__(self):
        res = "score: " + str(self.score)
        res += "\n control: " + str(self.control)
        res += "\n operations: " + str(self.operations)

        return res
