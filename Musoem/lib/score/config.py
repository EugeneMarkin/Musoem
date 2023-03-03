import re
from lib.operations.operations import *
from lib.playables.playable import Playable
from FoxDot import Pattern, P

class Config:

    def __init__(self, path):
        print("foo bar")
        self.path = path

    def evaluate(self, playables):
        # first create local variables for score objects that may be used in the script
        for p in playables:
            command = "%s = %s" % (p.keyword, "p")
            exec(command)
        # now load the script and execute it
        with open(self.path, "r") as file:
            script = file.read()
        exec(script)
        # collect the operations that are defined in the script
        operations = []
        new_playables = []
        new_vars = re.findall(r'(.+)?\s=.', script)
        for v in new_vars:
            if re.findall(r'[\.\[\]]', v) != []:
                continue
            obj = locals()[v]
            if isinstance(obj, Operation):
                obj.keyword = v
                operations.append(obj)

            elif isinstance(obj, Playable):
                obj.keyword = v
                new_playables.append(obj)
        return (new_playables, operations)
