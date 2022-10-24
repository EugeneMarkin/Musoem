from command import Command, OrList
from section import Section, SectionGroup
from operations import SectionOperation, ControlOperation
from FoxDot import Pattern
from now_playing import NowPlaying
from command_map import CommandMap

# Command interpreter takes a nested list of score sections, random access lists
# and operations, which can theoretically be combined in any order
# Since we're aiming at the natural language processing, we need to handle the arbitrary
# combinations of sections and operations and find a somewhat working interpretation for the result

class CommandInterpreter:

    def __init__(self, map: CommandMap):
        self.map = map

    def parse_command(self, command: Command):
        actions = command.actions
        sections = Pattern([])
        operations = Pattern([])
        # The actions array is the top-level sequence of events
        # that are separated by a comma in the statement
        for action in actions:
            # each action in sequence is a tuple -
            # a cluster of events that are triggered together
            if len(action) == 1:
                # if there is only one item in the tuple
                # we proceed to parse that item
                res = self._parse_rand_list(action[0])
                print("result of parse_rand_list", res)
            else:
                # otherwise we parse the tuple
                res = self._parse_tuple(action)
                print("result of parse_tuple", res)

            s, o = self._parse_result(res)
            print("result of _parse_result", s, o)
            sections = sections | s
            operations = operations | o

        if len(sections) > 0:
            section = self._sequence_sections(sections)
            print("top level section is", section, "operations: ", operations)
            self._apply_operations_to_sections(operations, Pattern([section]))
            if command.loop:
                self._find_last_section(section)._times = None
            NowPlaying.add(section)

        elif len(operations) > 0:
            print("got operations and no sections")
            print("will apply ", operations, "to the top section in the currently playing")
            last_section = NowPlaying.last_section()
            for operation in operations:
                last_section.apply(operation)


    def _parse_tuple(self, tuple):
        # as we parse the tuple we need to trigger the events together
        trigger_operations = Pattern([])
        trigger_sections = Pattern([])
        for rand_list in tuple:
            s, o = self._parse_result(self._parse_rand_list(rand_list))
            trigger_sections = trigger_sections | s
            trigger_operations = trigger_operations | o

        if len(trigger_sections) > 0:
            self._apply_operations_to_sections(trigger_operations, trigger_sections)
            return self._add_sections(trigger_sections)

        elif len(trigger_operations) > 0:
            return trigger_operations


    def _parse_rand_list(self, rand_list):
        # randomly pick one object from the array for now
        # TODO: make it possible for the code to pick a random object from
        # this list at each loop iteration (if there is a loop)
        sequence = rand_list.get()
        return self._parse_sequence(sequence)

    def _parse_sequence(self, seq):
        print("parse sequence", seq)
        sections = Pattern([])
        section_operations = Pattern([])

        for keyword in seq:
            s,o = self._parse_result(self._parse_keyword(keyword))
            sections = sections | s
            section_operations = section_operations | o
        print("parse sequence result: ", sections, section_operations)
        if (len(sections) > 0):
            self._apply_operations_to_sections(section_operations, sections)
            return self._sequence_sections(sections)
        elif (len(section_operations) > 0):
            # if there are no sections we need to apply the operations to sections
            # in another layer or to currently playing section
            # to apply operations to something
            return section_operations


    def _apply_operations_to_sections(self, operations, sections):
        # The opearations list is applied to sections list in the FoxDot way
        # the out of bound indices start from the beggining of the list
        # e.g. if we have 4 sections and 2 operations, the operations will apply like:
        # 1st op. to 1st sec., 2nd op. to 2nd sec., 1st op. to 3rd sec., 2nd op. to 4th sec.
        # if we have 5 opearations and 2 sections:
        # 1st, 3rd and 5th op. to 1st sec. and 2nd and 4th op. to 2nd sec.
        if len(operations) == 0:
            return sections
        print("len of operations ", len(operations), " len of sections ", len(sections))
        for i in range(0,max(len(sections), len(operations))):
            sections[i].apply(operations[i])
        return sections

    def _sequence_sections(self, sections):
        for i in range(1,len(sections)):
        # chain section to play after each other
            (sections[i-1] * 1) >> (sections[i] * 1)
        return sections[0]

    def _add_sections(self, sections):
        section_group = sections[0]
        for i in range(1, len(sections)):
            next = sections[i]
            section_group = section_group + next
        return section_group

    def _parse_result(self, result):
        sections = Pattern([])
        operations = Pattern([])
        if isinstance(result, Section) or isinstance(result, SectionGroup):
            sections.append(result)
        # or an operation, in which case we need to figure out what to apply it to
        elif isinstance(result, SectionOperation):
            operations.append(result)
        elif isinstance(result, ControlOperation):
            NowPlaying.add(result)
        elif isinstance(result, Pattern):
            for item in result:
                list_sections, list_operations = self._parse_result(item)
                if len(list_sections) > 0:
                    print("Something went wrong when parsing sections", list_sections)
                for operation in list_operations:
                    operations.append(operation)
        return sections, operations


    def _parse_keyword(self, keyword):
        if keyword in self.map.score.keys():
            return self.map.score[keyword].copy()
        elif keyword in self.map.operations.keys():
            return self.map.operations[keyword].copy()
        elif keyword in self.map.control.keys():
            return self.map.control[keyword].copy()
        else:
            return None

    def _find_last_section(self, obj):
        if isinstance(obj, Section) or isinstance(obj, SectionGroup):
            next = obj._next
            last_section = obj
            while next is not None:
                last_section = next
                next = next._next
            return last_section
        elif isinstance(obj, Pattern):
            return self._find_last_section(obj[-1])
