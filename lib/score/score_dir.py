import os
from score import MusicXMLScore

class ScoreDir:
    def __init__(self, path):
        dir = os.listdir(path)
        # list all files in the directory
        for item in dir:
            # skip system files
            if item[0] == ".":
                continue
            if not os.path.isdir(folder_path + "/" + item):
                # there is file in the dir that might be a score or config
                if ".musicxml" in file:
                    # the file is a score
                    self.score = MusicXMLScore(path + "/" + item)
                    continue
                elif ".json" in item:
                    # implement the json parsing of config
                    continue
            # all directories at this level should be instrument dirs
            instrument_path = folder_path + "/" + item
            instrument_dir = os.listdir(instrument_path)
            if "sample" in instrument:
                self.sections.update(self.load_audio_files(instrument_dir, instrument, instrument_path))
            else "midi" in instrument:
                self.sections.update(self.load_midi_files(instrument_dir, instrument, instrument_path))
