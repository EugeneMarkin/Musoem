import re
from enum import Enum
import random
from command import Command, OrList
from interpreter import CommandInterpreter, CommandMap, NowPlaying
from section import Section, SectionOperation, ControlOperation, SectionStub

class TextPipe:

    # TODO: parse multi-line text so that it will schedule events resulting
    # from each line

    def __init__(self, map):
        self.interpreter = CommandInterpreter(map)

    def parse_line(self, line):

        # parse the last character in the line, which is a punctuation mark
        # it could be either "." (one repeat) or "...." (4 repeats)
        # or "!" crescendo or "?" diminuendo
        # if there's no punctuation mark in the end of the line, it means loop

        command = Command()
        res1 = re.findall(r'^([^\.\?\!]+)([\.\?\!]+)\s?$', line)
        if len(res1) > 1:
            print("wrong command")
        elif len(res1) == 0:
            command.reps = None
            command.dynamic_changes = None
            command.actions = self._parse_expression(line)
        else:
            rep_str = res1[0][1]
            command.reps = len(rep_str) if len(rep_str) > 0 else None
            command.dynamic_changes = self._parse_symbols(rep_str)
            expression = res1[0][0]
            command.actions = self._parse_expression(expression)
        print(command)
        self.interpreter.parse_command(command)

    # a word might mean either a section of the score
    # or an algorithmic function

    def _parse_expression(self, expr):
        # coma means sequencing of events
        sequence = []
        for a in expr.split(","):
            print("a is ", a)
            tup = []
            for b in a.split(" and "):
                print("b is ", b)
                list = OrList([])
                for c in b.split(" or "):
                    print("c is ", c)
                    list.append(c.split(" "))
                tup.append(list)
            sequence.append(tuple(tup))
        return sequence



    def _parse_symbols(self, string):
        dyn_change = []
        for s in string:
            if s == "!":
                dyn_change.append("cresc")
            elif s == "?":
                dyn_change.append("dim")
            else:
                dyn_change.append(None)
        return dyn_change

test_map = CommandMap()
test_map.score = {"something" : SectionStub([], keyword = "something"),
                  "in" : SectionStub([], keyword = "in"),
                  "way" : SectionStub([], keyword = "way"),
                  "she" : SectionStub([], keyword = "she"),
                  "moves" : SectionStub([], keyword = "moves")}

test_map.operations = {"reverse" : SectionOperation("reverse"),
                       "transpose" : SectionOperation("transpose")}

test_map.control = {"accel" : ControlOperation("accel"),
                    "ritt" : ControlOperation("ritt")}

text_pipe = TextPipe(test_map)

text_pipe.parse_line("something in the way she moves")
print(NowPlaying.display())
