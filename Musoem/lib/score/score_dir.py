import os
import re
from FoxDot import Clock, Pattern
from .score import MusicXMLScore, FileScore
from .config import Config
from ..command.command_map import CommandMap
from ..util.utils import get_bpm_from_path

# This class represents a file directory containing any type of score
# It is used by the File->Open dialog to load up music data into Musoem
class ScoreDir:
    def __init__(self, path):
        self.path = path
        self.bpm = None
        self.configs = None
        if not os.path.isdir(path):
            raise Exception("no file at path ", path)

    # loads the score directory and parses it into playables and
    # config files
    def load(self) -> CommandMap:
        playables = []
        configs = []
        dir = os.listdir(self.path)
        # list all files in the directory
        for item in dir:
            # skip system files
            if item[0] == ".":
                continue
            # a file in the dir that might be a score or config
            if not os.path.isdir(self.path + "/" + item):
                if ".musicxml" in item:
                    # the file is a score
                    playables += MusicXMLScore(self.path + "/" + item).playables
                    continue
                elif ".py" in item:
                    # implement the json parsing of config
                    conf = Config(self.path + "/" + item)
                    configs.append(conf)
                    continue
            # all directories at this level should be instrument dirs
            any_bpm = get_bpm_from_path(self.path)
            if any_bpm != []:
                self.bpm = int(any_bpm[0])
            else:
                self.bpm = Clock.bpm
            playables += FileScore(self.path).playables

        self.configs = configs
        (new_playables, operations) = self._execute_configs(configs, playables)
        playables += new_playables
        if self.bpm:
            for p in playables:
                if p.bpm is None or p.bpm == Pattern([]):
                    p.bpm = [self.bpm]
        cm = CommandMap(playables, operations)
        return cm

    def _execute_configs(self, configs, playables):
        operations = []
        new_playables = []
        for config in configs:
            (ps, ops) = config.evaluate(playables)
            new_playables += ps
            operations += ops
        playables += new_playables
        return new_playables, operations

    def update_configs(self, command_map):
        if self.configs:
            (new_playables, operations) = self._execute_configs(self.configs, list(command_map.playables.values()))
            # TODO: move the dict zip to utils
            command_map.operations = dict(zip(list(map(lambda x: x.keyword, operations)), operations))
            command_map.playables.update(dict(zip(list(map(lambda x: x.keyword, new_playables)), new_playables)))
        return command_map
