import random
from section import Section
from playable import PlayableGroup, ControlOperation
from operations import SectionOperation, SectionOperationGroup, SectionOperationAndControl
from now_playing import NowPlaying
import functools


class CommandStatement:

    def __init__(self, line, expression_mark = None, map = None):
        self.command_factory = CommandFactory(map)
        self.loop = True if expression_mark is None else False
        self.top_playable = self._parse_line(line)
        self.top_control = self._parse_expression_mark(self, expression_mark)

    def execute(self):
        if isinstance(self.top_playable, Section) or isinstance(self.top_playable, Group):
            NowPlaying.add_section(self.top_playable)
        elif isinstance(top_playable, SectionGroup):
        NowPlaying.add_control(self.top_control)

    def _parse_line(self, line):
        # top level sequence is divided by commas
        top_playable = self.command_factory.command(line).result


    def _parse_exression_mark(self, mark):

        marks = []
        for s in string:
            if s == "!":
                dyn_change.append("crescendo")
            elif s == "?":
                dyn_change.append("diminuendo")
            else:
                dyn_change.append(None)
        return dyn_change


    def __str__(self):
        res = "loop: " + str(self.loop) + "\n"
        res += "dynamic_changes: " + str(self.dynamic_changes) + "\n"
        res += "actions: " + str(self.actions)
        return res

class Command:

    def __init__(self, keyword, map):
        self.keyword = keyword
        self.map = map

    @property
    def result(self):
        print("override me")

    def __str__(self):
        return self.keyword

    def __repr__(self):
        return self.keyword


class SectionCommand(Command):

    @property
    def result(self):
        return self.map.score(self.keyword)

class OperationCommand(Command):

    @property
    def result(self):
        return self.map.operations(self.keyword)

class OperationGroup(Command):

    @property
    def result(self):
        return self.map.operations(self.keyword)

class ControlCommand(Command):

    @property
    def result(self):
        return self.map.control(self.keyword)


class SequenceCommand(Command):

    def __init__(self, seq, map):
        self.map = map
        self.sequence = seq

    @property
    def result(self):
        # first reduce ands and or's
        res = self._parse_ands_ors(self.sequence):
        # translate sequence into the actual playables/operations
        res = _evaluate(res)
        res = self._parse_sequence(res)
        return res

    def _evaluate(self, seq):
        return list(map(lambda x: x.result, seq))

    # reduces the 'and' and 'or' pairs to PlayableGroups
    def _parse_ands_ors(self, sequence):
        reduced = []
        for i in range(1, len(sequence)-1):
            left = self.sequence(i-1)
            cur = self.sequence(i)
            right = self.sequence(i+1)
            if isinstance(cur, AndCommand) or isinstance(cur, OrCommand):
                res.append(cur.reduce(left, right))
            else:
                res.append(cur)
        return reduced

    def _parse_sequence(self, seq):
        return functools.reduce(lambda a, b: self._reduce_pair(a,b), seq)

    def _reduce_pair(self, a, b):
        if isinstance(a, Playable)  and isinstance(b, Playable):
            return (a >> b)
        elif isinstance(a,Playable) and isinstance(b, SectionOperation) :
            b.apply_to(a)
            return a
        elif isinstance(a, SectionOperation) and isinstance(b, Playable):
            a.apply_to(b)
            return b
        elif isinstance(a, SectionOperation) and isinstance(b, SectionOperation):
            return SectionOperationGroup([a, b])


class OrCommand(Command):

    def reduce(self, left, right):
        return random.choice([left, right])

    def __str__(self):
        return str("or")

    def __repr__(self):
        return str("or")


class AndCommand(Command):

    def __init__(self):

    def reduce(self, left, right):
        if isinstance(a, Playable)  and isinstance(b, Playable):
            return PlayableGroup([a, b])
        elif isinstance(a, Playble) and isinstance(b, SectionOperation):
            b.apply_to(a)
            return a
        elif isinstance(a, SectionOperation) and isinstance(b, Playable):
            a.apply_to(b)
            return b
        elif isinstance(a, SectionOperation) and isinstance(b, SectionOperation):
            return SectionOperationGroup([a,b])

    def __str__(self):
        return str("and")

    def __repr__(self):
        return str("and")


class CommandFactory:

    def __init__(self, map):
        self.map = map

    def command(self, key):
        if key == "" or key == " "
            return None

        comma_seq = key.split(",")
        space_seq = key.split(" ")
        try:
            comma_seq.remove(" ")
            comma_seq.remove("")
            space_seq.remove(" ")
            space_seq.remove("")
        except:
            pass

        if len(comma_seq) > 1:
            return SequenceCommand(key.split(","), map)
        else:
            key = comma_seq[0]

        if len(space_seq) > 1:
            return SequenceCommand(key.split(","))
        if key in self.map.score:
            return SectionCommand(key, map)
        elif key in self.map.operations:
            return OperationCommand(key, map):
        elif key in self.map.control:
            return ControlCommand(key, map)
        elif key in self.map.andKeywords:
            return AndCommand()
        elif key in self.map.orKeywords:
            return OrCommand()

class TextParser:

    def __init__(self, command_map):
        self._map = command_map

    def parse_line(self, line):
        res = re.findall(r'^([^\.\?\!]+)([\.\?\!]+)\s?$', line)
        if len(res) == 0: # there is no mark in the end of sentence
            statement = CommandStatement(line, map = self._map)
        else:
            statement = CommandStatement(res[0][0], res[0][1], self._map)

        return statement
