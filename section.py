from measure import Measure
from FoxDot import Pattern
from FoxDot import Player
from FoxDot import FileSynthDef
from FoxDot import Env
from FoxDot import Scale
from FoxDot import MidiOut
from FoxDot import Clock
from FoxDot import rest
from section_player import SectionPlayer
from now_playing import NowPlaying

# A Section is a FoxDot-friendly class that represents a section of music for
# a signle part and single voice.

# Section contains FoxDot patterns that can be passed to a Player object:
    # pitch, octave, duration, bpm

class Section(object):

    def __init__(self, measures:[Measure], instrument_key = None, keyword = None):
        self.player = SectionPlayer()
        self.degree = Pattern([])
        self.oct = Pattern([])
        self.dur = Pattern([])
        self.bpm = Pattern([])
        # TODO: implement this
        self.ts = Pattern([])
        self.sus = Pattern([])
        self.amp = Pattern([]) # TODO: add parsing of dynamics to score parser
        self.wait = 0
        self.keyword = keyword
        self.operations = {}

        self._next= None
        self._times = None
        self._isplaying = False
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

    def play(self, times = None):
        if self.wait != 0:
            Clock.future(self._get_clock_beats(self.wait), self.play, args=[times])
            self.wait = 0
            return self

        if self._isplaying:
            print("Section already playing")
            return self
        self._isplaying = True

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
        if times is not None:
            delay_beats = self._get_clock_beats(times * self._total_dur)
            Clock.future(delay_beats, self.stop)


        return self

    def apply(self, operation):
        self.operations[operation.keyword] = operation
        print("applying operation ", operation.keyword, operation, "to section ", self.keyword)

    def reset(self, operation_key = None):
        # TODO: impolement the operation reset
        if operation is not None:
            print("resetting operation", operation_key)
        else:
            for operation in list(self.operations.values()):
                print("resetting operation", operation.keyword)

    def display(self):
        res = self.keyword + " "
        print("section ", self.keyword, "operations ", self.operations)
        for operation in list(self.operations.values()):
            res += operation.keyword + " "

        if self._next is not None:
            res += self._next.display()
        return res

    def copy(self):
        return self.__class__(self._measures, instrument_key = self._instrument_key, keyword = self.keyword)

    @property
    def _average_tempo(self):
        return sum(self.bpm)/len(self.bpm)

    def _get_clock_beats(self, beats):
        return beats * Clock.bpm / self._average_tempo

    @property
    def _total_dur(self):
        res = 0
        for el in self.dur:
            if (isinstance(el, float) or isinstance(el, int)):
                res += el
            elif isinstance(el, rest):
                res += el.dur
        return res

    def stop(self):
        self._isplaying = False
        self.player.stop()
        NowPlaying.remove(self.keyword)
        if self._next is not None:
            self._next.play(self._next._times)
            self._next = None

    def cancel(self):
        self._isplaying = False
        self.player.stop()

    def once(self):
        self.play(1)

    def reset(self):
        self.cancel()
        print("resetting section")

    def __call__(self, times = None):
        return self.play(times)

    def __rshift__(self, section):
        if (not isinstance(section, Section)
            and not isinstance(section, SectionGroup)):
                print("Warning: can't schedule ", section, "after Section")
                return self
        if self == section:
            print("Warning: can't schedule section after itself")
            return self
        self._next = section
        return section

    def __add__(self, section):
        if not isinstance(section, Section):
            print("Warning: can't add Section and", section)
            return self
        if self == section:
            print("Warning: can't add section to itself")
            return self
        return SectionGroup([self, section], self.keyword + " and " + section.keyword)

    def __mul__(self, times):
        if isinstance(times, int):
            self._times = times
        return self

    def __mod__(self, delay):
        if (isinstance(delay, float) or isinstance(delay, int)):
            self.wait = delay
        return self

    def __invert__(self):
        self.stop()

    # bypass the attributes other than player and instrument to the player
    # so when live coding we can apply pattern operations to the section object itself
    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if (attr != "player" and attr != "instrument"
            and attr != "_times" and attr != "_next"):
            self.player.__setattr__(attr, value)

    def __getattr__(self, name):
        return self.player.__getattribute__(name)

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

class SectionGroup(object):

    def __init__(self, sections, keyword = None):
        self._sections = sections
        self._times = None
        self._next = None
        self._isplaying = False
        self.keyword = keyword

    def play(self, times = None):
        if self._isplaying:
            print("Group already playing")
            return self
        self._isplaying = True

        for section in self._sections:
            section(section._times)

        if times is not None:
            dur = max(list(map(lambda x: x._get_clock_beats(x._total_dur), self._sections)))
            Clock.future(times * dur, self.stop)
        else:
            # TODO: simplify this by adding a function that returns total clock beats
            all_times = list(map(lambda x: x._times, self._sections))
            all_durs = list(map(lambda x: x._get_clock_beats(x._total_dur), self._sections))
            if None not in all_times:
                durs = [t * d for t, d in zip(all_times, all_durs)]
                Clock.future(max(durs), self.stop)
        return self

    def stop(self):
        self._isplaying = False
        for section in self._sections:
            section.stop()
        if self._next is not None:
            self._next.play(self._next._times)
            self._next = None

    def cancel(self):
        for section in self._sections:
            section.cancel()

    def display(self):
        res = ""
        for section in self._sections:
            res += section.display() + "\n"
        return res

    def apply(self, operation):
        for section in self._sections:
            section.apply(operation)

    def copy(self):
        sections_copy = []
        for section in self._sections:
            sections_copy.append(section.copy())
        return self.__class__(sections_copy)

    def reset(self):
        print("resetting section group")


    def __call__(self):
        self.play()

    def __add__(self, other):
        if (other == self or other in self._sections):
            print("Warning: section already in group")
            return self

        sections = self._sections.copy()
        if isinstance(other, Section):
            sections.append(other)
            return SectionGroup(sections)
        elif isinstance (other, SectionGroup):
            sections.extend(other._sections)
            return SectionGroup(sections)
        else:
            print("Warning: can't add GroupSection and", other)
            return self

    def __mul__(self, times):
        if not isinstance(times, int):
            return self
        self._times = times

    def __rshift__(self, next):
        if (not isinstance(next, Section)
            and not isinstance(next, SectionGroup)):
                print("Warning: can't schedule ", next, "after SectionGroup")
                return self
        if (self == next or next in self._sections):
            print("Warning: can't schedule same section after itself")
            return self
        self._next = next
        return next

    def __invert__(self):
        self.stop()

class SectionGroupStub(SectionGroup):

    def play(self, times = None):
        print("playing section group")

    def __add__(self, section):
        sections = self._sections.copy()
        if isinstance(other, Section):
            sections.append(other)
            return SectionGroupStub(sections)
        elif isinstance (other, SectionGroup):
            sections.extend(other._sections)
            return SectionGroupStub(sections)
        else:
            print("Warning: can't add GroupSection and", other)
            return self
