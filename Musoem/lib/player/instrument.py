from FoxDot import SynthDef, FileSynthDef, MidiOut, Env, SynthDefs
import os
from ..base.constants import MUSOEM_SYNTHS_DIR

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
            if os.path.isfile(filename):
                self.synthdef.env = Env.mask()
            else:
                print("WARNING: there is no instrument named ", key, "will fall back to piano")
                self.synthdef = SynthDef("keys")

    def __str__(self):
        return self.key

    def __eq__(self, other):
        if self.synthdef == MidiOut and other.synthdef == MidiOut:
            return True
        elif self.synthdef == MidiOut or other.synthdef == MidiOut:
            return False
        else:
            return self.synthdef.filename == other.synthdef.filename

    @classmethod
    def musoem_synths(self):
        return list(map(lambda x: os.path.splitext(x)[0], os.listdir(MUSOEM_SYNTHS_DIR)))

    @classmethod
    def sampler_synths(self):
        return ["sampler"]

    @classmethod
    def all_synths(self):
        return Instrument.musoem_synths() + list(SynthDefs.keys())
