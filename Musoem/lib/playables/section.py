from ..score.measure import Measure
from FoxDot import Pattern, Player, FileSynthDef, Env, Scale, MidiOut, Clock, rest
from ..player.section_player import SectionPlayer
from .playable import Playable

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

# Section contains FoxDot patterns that can be passed to a Player object:
    # pitch, octave, duration, bpm

pattern_keys = ["degree", "oct", "dur", "sus", "bpm", "amp"]

class Section(Playable):

    def __init__(self, measures:[Measure], instrument_key = None, keyword = "None"):
        super().__init__(keyword)

        self.player = SectionPlayer()

        self.vals = [Pattern([]) for _ in pattern_keys]
        self.patterns = dict(zip(pattern_keys, self.vals))

        # TODO: implement this
        self.ts = Pattern([])

        self._measures = measures
        self.instrument_key = instrument_key

        for mes in measures:
            self.degree.extend(mes.degree)
            self.oct.extend(mes.oct)
            self.dur.extend(mes.dur)
            self.sus.extend(mes.sus)
            self.bpm.extend(mes.bpm)
            self.amp.extend(mes.amp)

        if instrument_key is not None:
            if "midi" in instrument_key:
                split_key = instrument_key.split(" ")
                if (len(split_key) != 2):
                    return
                self.add_midi_out(int(split_key[1]) - 1) # -1 because FoxDot counts midi channels from 0
            else:
                self.add_instrument(instrument_key)

    def add_instrument(self, instr):
        self.instrument = FileSynthDef(instr)
        self.instrument.env = Env.mask()
        self.instrument.add()

    def add_midi_out(self, channel):
        self.instrument = MidiOut
        self.midi_channel = channel

    def play(self, times = None):
        if super().play() is None:
            return self

        if self.instrument is None:
            print("Can't play. Add an instrument first")
            return self
        self.player = SectionPlayer()
        self.player >> self.instrument(channel = self.midi_channel,
                                       degree = self.degree,
                                       oct = self.oct,
                                       dur = self.dur,
                                       sus = self.sus,
                                       bpm = self.bpm,
                                       amp = self.amp,
                                       scale = Scale.chromatic)
        print("playing ", self, self.player)
        return self

    def copy(self):
        return self.__class__(self._measures, instrument_key = self.instrument_key, keyword = self.keyword)

    @property
    def total_dur(self):
        if self._times == None:
            return None
        res = 0
        for el in self.dur:
            if (isinstance(el, float) or isinstance(el, int)):
                res += el
            elif isinstance(el, rest):
                res += el.dur
        return res * self._times

    def stop(self):
        if self._isplaying:
            self.player.stop()
        super().stop()

    @property
    def loop(self):
        self * -1
        return self

    # bypass the attributes other than player and instrument to the player
    # so when live coding we can apply pattern operations to the section object itself
    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if attr in pattern_keys:
            self.patterns[attr] = value
            self.player.__setattr__(attr, value)

    def __getattr__(self, name):
        if name in pattern_keys:
            return self.patterns[name]
        else:
            return None

    def __getitem__(self, key):
        if key in self.patterns:
            return self.patterns[key]
        else:
            return None

    def __setitem__(self, key, value):
        if key in self.patterns:
            self.__setattr__(key, value)

    def __str__(self):
        return "Section " + self.keyword

    @property
    def description(self):
        return str(self.patterns)

class SectionStub(Section):

    def play(self, times = None):
        print("playing section", self.keyword)

    def __add__(self, section):
        return SectionGroupStub([self, section], self.keyword + " and " + section.keyword)
