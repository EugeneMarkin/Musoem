from command import Command
from command import OrList

class CommandMap:
    def __init__(self):
        self.score = {}
        self.operations = {}

    # TODO: add load from file


class CommandInterpreter:

    def __init__(self, map: CommandMap):
        self.map = map

    def parse_command(self, command: Command):
        
