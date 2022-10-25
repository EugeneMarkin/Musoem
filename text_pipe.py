import re
from enum import Enum
import random
from command import Command, OrList
from interpreter import CommandInterpreter, NowPlaying
from section import Section, SectionStub
from operations import SectionOperation, ControlOperation
from command_map import CommandMap

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
        print("command is", res1)
        if len(res1) > 1:
            print("wrong command")
        elif len(res1) == 0:
            command.loop = True
            command.dynamic_changes = None
            command.actions = self._parse_expression(line)
        else:
            rep_str = res1[0][1]
            command.loop = False if len(rep_str) > 0 else True
            print("loop", command.loop)
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
                dyn_change.append("crescendo")
            elif s == "?":
                dyn_change.append("diminuendo")
            else:
                dyn_change.append(None)
        return dyn_change
