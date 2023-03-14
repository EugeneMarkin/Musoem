import re
from lib.operations.operations import *
from lib.playables.playable import Playable
from lib.playables.section import Section
from lib.playables.sample import Sample
from FoxDot import Pattern, P, PGroup, PxRand


class Container:

    def __init__(self, elements):
        self.elements = elements

    def __setattr__(self, attr, value):
        if attr != "elements":
            for el in self.elements:
                el.__setattr__(attr, value)
        else:
            super().__setattr__(attr, value)

class Config:

    def __init__(self, path):
        print("foo bar")
        self.path = path

    def evaluate(self, playables):
        # first create local variables for score objects that may be used in the script
        for p in playables:
            print("playable ", p, "kw is ", p.keyword)
            command = "%s = %s" % (p.keyword, "p")
            exec(command)
        # define special variables for setting params to multiple objects in the script
        all_p = Container(playables)
        sections = list(filter(lambda x: isinstance(x, Section), playables))
        all_sections = Container(sections)
        samples = list(filter(lambda x: isinstance(x, Sample), playables))
        all_samples = Container(samples)
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
