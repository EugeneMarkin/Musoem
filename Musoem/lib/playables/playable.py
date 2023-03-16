from FoxDot import Pattern, Clock
from functools import reduce
from ..player.section_player import SectionPlayer
from ..player.now_playing import NowPlaying
from ..base.entity import Entity

# A base class for Playable objects

class Playable(Entity):

    def __init__(self, keyword):
        super().__init__(keyword)
        # here and elsewhere we use __dict__ subscript to define instance variables
        # because of the overriden __setattr__, which needs to distinguish between
        # instance variables and params sent to player
        self.__dict__["wait"] = 0 # a delay to wait before starting to play
        self.__dict__["_next"] = None # next Playable object after this one
        self.__dict__["_parent"] = None # the Playable that will trigger this playback of this object when finished
        self.__dict__["_times"] = 1 # the number of repeats (gets overriden if different value is passed to play())
        self.__dict__["_isplaying"] = False
        self.__dict__["operations"] = {}

    def play(self):
        if self.wait != 0:
            Clock.future(self._get_clock_beats(self.wait), self.play)
            self.wait = 0
            return None

        if self._isplaying:
            print(self.keyword, " is already playing")
            return None
        self._isplaying = True

        self._parent = None

        if self._times is not None:
            delay_beats = self._get_clock_beats(self.total_dur)
            Clock.future(delay_beats, self.stop)

        NowPlaying.add(self)
        return self

    # stops the current playable and triggers the next thats linked to it
    def stop(self):
        if self._isplaying:
            self._isplaying = False
            NowPlaying.remove(self)
            if self._next is not None:
                self._next()
                self._next = None
        else:
            self.cancel()

    # stops the playable and doesn't trigger next
    # if it is not playing but is scheduled, it removes itself from the parent
    def cancel(self):
        if self._isplaying:
            self._isplaying = False
            NowPlaying.update()
        elif self._parent is not None:
            self._parent._next = None
            self._parent = None
            if self._next is not None:
                self._parent >> self._next

    # the represenation of the Playable in the performance window
    def display(self):
        res = [self]
        for op in self.operations.values(): res.append(op)

        if self._next is not None:
            res += self._next.display()
        return res

    @property
    def total_dur(self):
        print("override me")

    @property
    def average_tempo(self):
        print("override me")

    def apply_operation(self, operation):
        self.operations[operation.keyword] = operation
        operation.execute(self)

    @property
    def time_till_end(self):
        durs = []
        for p in self:
            if p._times is not None:
                durs.append(self._get_clock_beats(p.total_dur))
            else:
                return None
        return sum(durs)

    def _get_clock_beats(self, beats):
        return beats * Clock.bpm / self.average_tempo


    # call is duplicating the play function
    def __call__(self):
        self.play()

    @property
    def last(self):
        return iter(self)[-1]

    @property
    def root(self):
        cur = self
        while cur._parent is not None:
            cur = cur._parent
        return cur

    # set next schedulable after this one
    def __rshift__(self, other):
        if other in self:
            other = other.copy()
        self._next = other
        other._parent = self
        return other

    # set the _times parameter of self
    def __mul__(self, times):
        if isinstance(times, int):
            if times < 0: # loop
                self._times = None
            else:
                self._times = times
        return self

    # delay a schedulable
    def __mod__(self, delay):
        if (isinstance(delay, float) or isinstance(delay, int)):
            self.wait = delay
        return self

    # stop the schdulable
    def __invert__(self):
        self.stop()

    def __iter__(self):
        l = [self]
        next = self._next
        while next is not None:
            l.append(next)
            next = next._next
        return iter(l)

    def __next__(self):
        if self._next is None:
            raise StopIteration
        else:
            return self._next

    def __contains__(self, obj):
        for p in self:
            if obj == p:
                return True
        return False


class SoundObject(Playable):

    def __init__(self, instrument, keyword = "None"):
        super().__init__(keyword)
        self.__dict__["instrument"] = instrument
        self.__dict__["player"] = SectionPlayer()
        self.__dict__["params"] = {"degree" : Pattern([]), "dur" : Pattern([1])}

    # start playing with "times" repeats and "self.wait" delay
    def play(self):
        if not super().play():
            return

        self.player = SectionPlayer()
        if self.instrument is None:
            raise Exception("Can't play the section because there is no instrument")

        degree = self.params["degree"]
        kwargs = self.params.copy()
        kwargs.pop("degree")
        self.player >> self.instrument.synthdef(degree, **kwargs)


    def stop(self):
        if self._isplaying == True:
            self.player.stop()
        super().stop()


    @property
    def display_style(self):
        return "normal"

    # add playables together
    def __add__(self, p):
        return SoundGroup([self, p])


    def __setattr__(self, attr, val):
        if attr in self.__dict__:
            self.__dict__[attr] = val
        else:
            if not isinstance(val, Pattern):
                if isinstance(val, list):
                    val = Pattern(val)
                elif isinstance(val, int) or isinstance(val, float):
                    val = Pattern([val])
            self.params[attr] = val
            self.player.__setattr__(attr, val)

    def __getattr__(self, attr):
        print("getting attribute from ", attr)
        if attr in self.params:
            return self.params[attr]
        return None

    def __getitem__(self, key):
        return self.params[key]

    @property
    def average_tempo(self):
        return sum(self.bpm)/len(self.bpm)



class SoundGroup(Playable):

    def __init__(self, playables):
        super().__init__(reduce(lambda a,b: a.keyword + "," + b.keyword, playables))
        self.__dict__["playables"] = playables

    def play(self):
        if super().play() is None:
            return self

        for p in self: p()

        if self._times is not None:
            return self

        # TODO: simplify this by adding a function that returns total clock beats
        all_times = list(map(lambda x: x._times, self))
        if None not in all_times:
            all_durs = list(map(lambda x: x._get_clock_beats(x.total_dur), self))
            Clock.future(max(all_durs), self.stop)

        return self

    def stop(self):
        if self._isplaying:
            for p in self: ~p
        super().stop()


    def copy(self):
        return self.__class__(list(map(lambda p: p.copy(), self)))

    def append(self, other):
        if isinstance(other, SoundGroup):
            for p in other: self.append(p)
        else:
            self.playables.append(other)
            self.keyword += "," + other.keyword

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            for p in self.playables:
                p.__setattr__(key, value)

    def __add__(self, other):
        if other in self:
            other = other.copy()
        else:
            for pl in self:
                if other in pl:
                    other = other.copy()
        self.append(other)
        return self

    def __rshift__(self, other):
        if other is self:
            other = other.copy()
        else:
            for pl in self:
                if other in pl:
                    other = other.copy()

        return super().__rshift__(other)

    def __mul__(self, times):
        if times < 1:
            list(map(lambda p: p * -1, self))
        return super().__mul__(times)

    def __iter__(self):
        return iter(self.playables)

    def __contains__(self, obj):
        return obj in self.playables

    def display(self):
        return [self]

    def apply_operation(self, operation):
        for p in self:
            p.apply_operation(operation.copy())

    @property
    def total_dur(self):
        durs = list(map(lambda x: x.total_dur, self))
        if None not in durs:
            return max(durs)
        else:
            return None

    @property
    def average_tempo(self):
        tempos = list(map(lambda x: x.average_tempo, self))
        return sum(tempos)/len(tempos)

    @property
    def time_till_end(self):
        times = list(map(lambda x: x.time_till_end, self))
        return max(times)
