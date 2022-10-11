import re
from enum import Enum
import random
from command import Command
from command import OrList

class TextPipe:

    def parse_line(self, line):

        # parse the last character in the line, which is a punctuation mark
        # it could be either "." (one repeat) or "...." (4 repeats)
        # or "!" crescendo or "?" diminuendo
        # if there's no punctuation mark in the end of the line, it means loop
        command = Command()
        reps = 0
        res1 = re.findall(r'^([^\.\?\!]+)([\.\?\!]+)\s?$', line)
        if len(res1) > 1:
            print("wrong command")
        elif len(res1) == 0:
            command.reps = -1
            command.dynamic_changes = None
            command.actions = self._parse_expression(line)
        else:
            rep_str = res1[0][1]
            command.reps = len(rep_str)
            command.dynamic_changes = self._parse_symbols(rep_str)
            expression = res1[0][0]
            command.actions = self._parse_expression(expression)
        print(command)

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
