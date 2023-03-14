from ..operations.operations import *
from ..score.score import Score, FileScore
from ..operations.control_operations import crescendo

# This class represents the mapping between the input keywords and the music,
# that will be used in the current session.

class CommandMap:
    def __init__(self, playables, operations = {}):
        self.playables = dict(zip(list(map(lambda x: x.keyword, playables)), playables))
        self.operations = dict(zip(list(map(lambda x: x.keyword, operations)), operations))
        self.wait_mark = ";"
        self.control = {"!" : crescendo("!",dur = 10, fromval = "ppp", toval = "fff"),
                        "?" : crescendo("?", dur = 10, fromval = "fff", toval = "ppp")}
        self.andKeywords = ["and", "And"]
        self.orKeywords = ["or", "Or"]
        self.pause_time = 2 # in beats


    def add_control(self, list):
        for item in list:
            self.control[item.keyword] = item

    def add_operations(self, list):
        for item in list:
            self.operations[item.keyword] = item

    def __getitem__(self, key):
        res = None
        if key in self.playables:
            res = self.playables[key]
        elif key in self.operations:
            res = self.operations[key]
        elif key in self.control:
            res = self.control[key]
        return res

    def __str__(self):
        res = "playables: " + str(self.playables)
        res += "\n control: " + str(self.control)
        res += "\n operations: " + str(self.operations)

        return res
