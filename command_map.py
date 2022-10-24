from section import SectionStub
from operations import *


class CommandMap:
    def __init__(self):
        self.score = {}
        self.operations = {}
        self.control = {}

    # TODO: add load from file
test_map = CommandMap()
test_map.score = {"Mary" : SectionStub([], keyword = "Mary"),
                  "had" : SectionStub([], keyword = "had"),
                  "little" : SectionStub([], keyword = "little"),
                  "lamb" : SectionStub([], keyword = "lamb"),
                  "cow" : SectionStub([], keyword = "cow")}

test_map.operations = {"reverse" : SectionOperation("reverse"),
                       "transpose" : SectionOperation("transpose")}

test_map.control = {"accel" : ControlOperation("accel"),
                    "ritt" : ControlOperation("ritt")}


default_map = CommandMap()
default_map.operations = {"crescendo" : Crescendo(),
                          "diminuendo" : Diminuendo()}

# brian eno oblique strategies
