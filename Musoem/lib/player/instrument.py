from FoxDot import SynthDef, FileSynthDef, MidiOut, Env
from os import path

class Instrument:

    def __init__(self, key):
        self.key = key
        if "midi" in key:
            split_key = key.split(" ")
            if (len(split_key) != 2):
                print("WARNING: invalid midi instrument ", split_key)
                return
            self.synthdef = MidiOut
            self.midi_channel = int(split_key[1])
        else:
            self.synthdef = FileSynthDef(key)
            filename = self.synthdef.filename
            if path.isfile(filename):
                self.synthdef.env = Env.mask()
            else:
                print("WARNING: there is no instrument named ", key, "will fall back to piano")
                self.synthdef = SynthDef("piano")

    def __str__(self):
        return self.key

    def __eq__(self, other):
        if self.synthdef == MidiOut and other.synthdef == MidiOut:
            return True
        elif self.synthdef == MidiOut or other.synthdef == MidiOut:
            return False
        else:
            return self.synthdef.filename == other.synthdef.filename
