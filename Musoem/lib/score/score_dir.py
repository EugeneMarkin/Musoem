import os
import re
from .score import MusicXMLScore, FileScore
from .config import Config
from ..command.command_map import CommandMap

# This class represents a file directory containing any type of score
# It is used by the File->Open dialog to load up music data into Musoem
class ScoreDir:
    def __init__(self, path):
        self.path = path

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
            project_name = os.path.basename(self.path)
            any_bpm = re.findall(r'bpm=([0-9]+)', project_name)
            if any_bpm != []:
                bpm = int(any_bpm[0])
                playables += FileScore(self.path, bpm).playables
            else:
                playables += FileScore(self.path).playables

        print("parsed playables are: ", playables)
        operations = []
        new_playables = []
        for config in configs:
            (ps, ops) = config.evaluate(playables)
            new_playables += ps
            operations += ops
        playables += new_playables
        cm = CommandMap(playables, operations)
        return cm
