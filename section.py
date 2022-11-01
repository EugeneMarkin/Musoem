from measure import Measure
from FoxDot import Pattern, Player, FileSynthDef, Env, Scale, MidiOut, Clock, rest
from section_player import SectionPlayer
from playable import Playable

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

# Section contains FoxDot patterns that can be passed to a Player object:
    # pitch, octave, duration, bpm

class Section(Playable):

    def __init__(self, measures:[Measure], instrument_key = None, keyword = None):
        super().__init__(keyword)

        self.player = SectionPlayer()
        self.degree = Pattern([])
        self.oct = Pattern([])
        self.dur = Pattern([])

        # TODO: implement this
        self.ts = Pattern([])
        self.sus = Pattern([])
        self.amp = Pattern([]) # TODO: add parsing of dynamics to score parser

        self._measures = measures
        self._instrument_key = instrument_key

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

    @property
    def patterns(self):
        return [self.degree, self.oct, self.dur, self.sus, self.bpm, self.amp]

    def play(self, times = None):
        if super().play(times) is None:
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
        return self.__class__(self._measures, instrument_key = self._instrument_key, keyword = self.keyword)

    @property
    def total_dur(self):
        res = 0
        for el in self.dur:
            if (isinstance(el, float) or isinstance(el, int)):
                res += el
            elif isinstance(el, rest):
                res += el.dur
        return res

    def stop(self, keyword = None):
        if keyword == self.keyword or keyword is None:
            self.player.stop()
        else:
            ops = list(filter(lambda o: o.keyword == keyword, self.operations.values()))
            map(lambda o: o.reset(), ops)
        super().stop(keyword)

    # bypass the attributes other than player and instrument to the player
    # so when live coding we can apply pattern operations to the section object itself
#    def __setattr__(self, attr, value):
#        self.__dict__[attr] = value
#        if (attr != "player" and attr != "instrument"
#            and attr != "_times" and attr != "_next"):
#            self.player.__setattr__(attr, value)

#    def __getattr__(self, name):
#        return self.player.__getattribute__(name)

    def display(self):
        res = self.keyword + " "
        for op_kw in self.operations.keys():
            res += op_kw + " "
        if self._next is not None:
            res += self._next.display()
        return res

    @property
    def description(self):
        res = "degree: " + str(self.degree) + ", "
        res += "octave: " + str(self.oct) + ", "
        res += "duration: " + str(self.dur) + ", "
        res += "sustain: " + str(self.sus) + ", "
        res += "amp: " + str(self.amp) + ", "
        res += "bpm: " + str(self.bpm)
        return res

class SectionStub(Section):

    def play(self, times = None):
        print("playing section", self.keyword)

    def __add__(self, section):
        return SectionGroupStub([self, section], self.keyword + " and " + section.keyword)
