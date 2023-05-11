import random
import re
import functools

from ..playables.section import Section
from ..playables.playable import Playable
from ..operations.operations import Operation, OperationGroup
from ..player.now_playing import NowPlaying

class CommandStatement:

    def __init__(self, line, expression_mark = None, map = None):
        self.command_factory = CommandFactory(map)
        self.loop = True if expression_mark is None else False
        self.wait = True if expression_mark == map.wait_mark else False
        self.top_playable = self._parse_line(line)
        self.top_control = None
        if expression_mark:
            self.top_control = self._parse_line(expression_mark)

    def execute(self):
        if self.top_control:
            self.top_control()
        if isinstance(self.top_playable, Playable):
            if self.wait:
                NowPlaying.last() >> self.top_playable
                return
            if self.loop:
                self.top_playable * -1
            self.top_playable = self.top_playable.root
            self.top_playable()
        elif isinstance(self.top_playable, Operation):
            list(map(lambda p: p.apply_operation(self.top_playable.copy()), NowPlaying.all()))


    def _parse_line(self, line):
        # top level sequence is divided by commas
        command = self.command_factory.command(line)
        return command.result if command else None


    def __str__(self):
        res = "loop: " + str(self.loop) + "\n"
        res += "top_playable: " + str(self.top_playable) + "\n"
        res += "top_control: " + str(self.top_control)
        return res

class Command:

    def __init__(self, keyword, map):
        self.keyword = keyword
        self._map = map

    @property
    def result(self):
        return self._map[self.keyword].copy()


class SequenceCommand(Command):

    def __init__(self, seq, map):
        self._map = map
        print("seq ", seq)
        self.sequence = seq

    @property
    def result(self):
        res = []
        items = self.sequence.copy()
        print("sequence ", items)
        while len(items) > 2:
            left = items[0]
            cur = items[1]
            right = items[2]
            if isinstance(cur, CombinationCommand):
                pair = PairCommand(self._map, cur, left, right)
                items = [pair] + items[3:]
            else:
                res.append(left)
                items.pop(0)
        res += items
        res = list(filter(lambda x: not isinstance(x, CombinationCommand), res))
        res = list(map(lambda x: x.result, res))
        res = functools.reduce(self._reduce_pair, res)
        return res

    def _reduce_pair(self, a, b):
        print("===============reduce pair called")
        print("a is ", type(a), " ", a)
        print("b is ", type(b), " ", b)
        if isinstance(a, Playable)  and isinstance(b, Playable):
            a._next = b
            b._parent = a
            return b
        elif isinstance(a,Playable) and isinstance(b, Operation) :
            print("=================================================playable and operation")
            a.apply_operation(b)
            return a
        elif isinstance(a, Operation) and isinstance(b, Playable):
            print("=================================================playable and operation<-")
            b.apply_operation(a)
            return b
        elif isinstance(a, Operation) and isinstance(b, Operation):
            return a + b


class PauseSequenceCommand(SequenceCommand):

    @property
    def result(self):
        l = list(map(lambda x: x.result, self.sequence))
        for p in l[1:]:
            if isinstance(p, Playable):
                p % self._map.pause_time
        res = functools.reduce(self._reduce_pair, l)
        return res

class PairCommand(Command):

    def __init__(self, map, combination_command, left, right):
        self._map = map
        self.command = combination_command
        self.left = left
        self.right = right

    @property
    def result(self):
        return self.command.reduce(self.left.result, self.right.result)


class CombinationCommand(Command):

    def reduce(self, left, right):
        print("override me")

class OrCommand(CombinationCommand):

    def reduce(self, left, right):
        return random.choice([left, right])

    def __str__(self):
        return str("or")

    def __repr__(self):
        return str("or")

class AndCommand(CombinationCommand):

    def reduce(self, a, b):
        if isinstance(a, Playable)  and isinstance(b, Playable):
            return a + b
        elif isinstance(a, Playable) and isinstance(b, Operation):
            a.apply_operation(b)
            return a
        elif isinstance(a, Operation) and isinstance(b, Playable):
            b.apply_operation(a)
            return b
        elif isinstance(a, Operation) and isinstance(b, Operation):
            return OperationGroup([a,b])

    def __str__(self):
        return str("and")

    def __repr__(self):
        return str("and")


class CommandFactory:

    def __init__(self, map):
        self._map = map

    def command(self, key):
        if key == "" or key == " ":
            return None
        filt = lambda x: x != " " and x != ""
        comma_seq = list(filter(filt, key.split(",")))
        if len(comma_seq) > 1:
            l = self._list_commands(comma_seq)
            return PauseSequenceCommand(l, self._map)
        else:
            key = comma_seq[0]

        space_seq = list(filter(filt, key.split(" ")))
        if len(space_seq) > 1:
            l = self._list_commands(space_seq)
            return SequenceCommand(l, self._map)
        else:
            key = space_seq[0]
        if key in self._map.andKeywords:
            return AndCommand(key, self._map)
        elif key in self._map.orKeywords:
            return OrCommand(key, self._map)
        elif key in self._map.playables or key in self._map.operations or key in self._map.control:
            return Command(key, self._map)


    def _list_commands(self, seq):
        l = list(map(lambda x: self.command(x) , seq))
        l = list(filter(lambda x: x is not None, l))
        return l

class TextParser:

    def __init__(self, command_map):
        self.command_map = command_map

    def parse_line(self, line):
        res = re.findall(r'^([^\.\?\!\;]+)([\.\?\!\;]+)\s?$', line)
        statement = None
        if len(res) == 0: # there is no mark in the end of sentence
            statement = CommandStatement(line, map = self.command_map)
        else:
            statement = CommandStatement(res[0][0], res[0][1], map = self.command_map)
        return statement
