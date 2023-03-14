from FoxDot import SynthDef, FileSynthDef, MidiOut, Env
from os import path

class Instrument:

    def __init__(self, key):
        print("calling instrument init")
        if "midi" in key:
            print("if")
            split_key = key.split(" ")
            if (len(split_key) != 2):
                print("invalid midi instrument ", split_key)
                return
            self.synthdef = MidiOut
            self.midi_channel = int(split_key[1])
        else:
            self.synthdef = FileSynthDef(key)
            filename = self.synthdef.filename
            print("filename is ", filename)
            if path.isfile(filename):
                self.synthdef.env = Env.mask()
            else:
                print("WARNING: there is no instrument named ", key, "will fall back to piano")
                self.synthdef = SynthDef("piano")
