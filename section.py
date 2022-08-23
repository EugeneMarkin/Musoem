from measure import Measure
from FoxDot import Pattern
from FoxDot import Player
from FoxDot import FileSynthDef
from FoxDot import Env
from FoxDot import Scale
from FoxDot import MidiOut

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

# Section contains FoxDot patterns that can be passed to a Player object:
    # pitch, octave, duration, bpm

class Section(object):
    def __init__(self, measures:[Measure]):
        self.player = Player()

        self.degree = Pattern([])
        self.oct = Pattern([])
        self.dur = Pattern([])
        self.bpm = Pattern([])
        # TODO: implement this
        self.ts = Pattern([])
        self.sus = Pattern([])

        for mes in measures:
            self.degree.extend(mes.degree)
            self.oct.extend(mes.oct)
            self.dur.extend(mes.dur)
            self.sus.extend(mes.sus)
            self.bpm.extend(mes.bpm)


    def add_instrument(self, instr):
        self.instrument = FileSynthDef(instr)
        self.instrument.env = Env.mask()
        self.instrument.add()

    def add_midi_out(self, channel):
        self.instrument = MidiOut
        self.midi_channel = channel

    def play(self):
        if self.instrument is None:
            print("Can't play. Add an instrument first")
            return
        self.player >> self.instrument(channel = self.midi_channel,
                                       degree = self.degree,
                                       oct = self.oct,
                                       dur = self.dur,
                                       sus = self.sus,
                                       bpm = self.bpm,
                                       scale = Scale.chromatic)
        
    def stop(self):
        self.player.stop()

    # bypass the attributes other than player and instrument to the player
    # so when live coding we can apply pattern operations to the section object itself
    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if (attr != "player" or attr != "instrument"):
            self.player.__setattr__(attr, value)


    @property
    def description(self):
        res = "degree: " + str(self.degree) + ", "
        res += "octave: " + str(self.oct) + ", "
        res += "duration: " + str(self.dur) + ", "
        res += "sustain: " + str(self.sus)
        res += "bpm: " + str(self.bpm)
        return res
