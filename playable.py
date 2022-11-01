from FoxDot import Pattern, Clock
from now_playing import NowPlaying
from functools import reduce

# Control Operation is a keyword operation that
# affects the global parameters of sound/tempo/dynamics
# regardless of the currently playing section(s)

# Control operation is a Playable
# which means that it can be added, or sequenced
# with Section objects

# A base class for Playable objects:
# Section, SectionGroup, ControlOperation

class Playable(object):

    def __init__(self, keyword = None):
        self.keyword = keyword
        self.wait = 0 # a delay to wait before starting to play
        self._next = None # next Playable object after this one
        self._parent = None
        self._times = 1 # the number of repeats (gets overriden if different value is passed to play())
        self._isplaying = False
        self.operations = {}
        self.bpm = Pattern([])

    # start playing with "times" repeats and "self.wait" delay
    def play(self, times = None):
        if self.wait != 0:
            Clock.future(self._get_clock_beats(self.wait), self.play, args=[times])
            self.wait = 0
            return None

        if self._isplaying:
            print(self.keyword, " is already playing")
            return None
        self._isplaying = True

        self._parent = None

        if times is not None:
            delay_beats = self._get_clock_beats(times * self.total_dur)
            Clock.future(delay_beats, self.stop)

        return self

    # stops the current playable and triggers the next thats linked to it
    def stop(self, keyword = None):
        if keyword is None or keyword == self.keyword:
            self._isplaying = False
            NowPlaying.remove(self.keyword)
            if self._next is not None:
                self._next.play(self._next._times)
                self._next = None
            return

        l = list(filter(lambda p: p.keyword == keyword, self))
        if len(l) > 0:
            for p in l: p.cancel()
        else:
            filtered = list(filter(lambda p: keyword in p.operations, self))
            for f in filtered: f.operations[keyword].reset()


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
        res = self.keyword + " "

        if self._next is not None:
            res += self._next.display()
        return res

    @property
    def root(self):
        cur = self
        while cur._parent is not None:
            cur = cur._parent
        return cur

    @property
    def last(self):
        return iter(self)[-1]

    # call is duplicating the play function
    def __call__(self, times = None):
        self.play(times)

    # set next playable after this one
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

    # add playables together
    def __add__(self, section):
        return PlayableGroup([self, section])

    # delay a playable
    def __mod__(self, delay):
        if (isinstance(delay, float) or isinstance(delay, int)):
            self.wait = delay
        return self

    # stop the playable
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

    @property
    def average_tempo(self):
        return sum(self.bpm)/len(self.bpm)

    def _get_clock_beats(self, beats):
        return beats * Clock.bpm / self.average_tempo

    @property
    def total_dur(self):
        print("override me")

    @property
    def time_till_end(self):
        durs = []
        for p in self:
            if p._times is not None:
                durs.append(self._get_clock_beats(p._times * p.total_dur))
            else:
                return None
        return sum(durs)

class PlayableGroup(Playable):

    def __init__(self, playables):
        super().__init__(reduce(lambda a,b: a.keyword + b.keyword, playables))
        self.playables = playables

    def play(self, times = None):
        if self._isplaying:
            print("Group already playing")
            return self
        self._isplaying = True

        for p in self: p(p._times)

        if times is not None:
            dur = max(list(map(lambda x: x._get_clock_beats(x.total_dur), self)))
            Clock.future(times * dur, self.stop)
            return self

        # TODO: simplify this by adding a function that returns total clock beats
        all_times = list(map(lambda x: x._times, self))
        all_durs = list(map(lambda x: x._get_clock_beats(x.total_dur), self))
        if None not in all_times:
            durs = [t * d for t, d in zip(all_times, all_durs)]
            Clock.future(max(durs), self.stop)
        return self

    def stop(self, keyword = None):
        if keyword is None or keyword == self.keyword:
            self._isplaying = False
            for p in self: ~p
            if self._next is not None:
                self._next.play(self._next._times)
                self._next = None
            return
        for p in self: p.stop(keyword)

    def cancel(self):
        for p in self: p.cancel()

    def copy(self):
        return self.__class__(list(map(lambda p: p.copy(), self)))

    def __add__(self, other):
        if other in self:
            other = other.copy()
        else:
            for pl in self:
                if other in pl:
                    other = other.copy()
        return self.__class__([self, other])

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

    @property
    def total_dur(self):
        return max(list(map(lambda x: x.total_dur, self)))

    @property
    def average_tempo(self):
        tempos = list(map(lambda x: x.average_tempo, self))
        return sum(tempos)/len(tempos)

    @property
    def time_till_end(self):
        times = list(map(lambda x: x.time_till_end, self))
        return max(times)


class ControlOperation(Playable):

    def __init__(self, keyword, control, dur, kwargs = {}):
        super().__init__(keyword)
        self.control = control
        self.kwargs = kwargs
        self.dur = dur

    def play(self, times = None):
        if super().play() is None:
            return self
        self.execute()

    def execute(self):
        print("override me")

    def stop(self, keyword = None):
        super().stop(keyword)

    def finish(self):
        print("override me")

    def cancel(self):
        # not sure how to do that
        super().cancel()

    def copy(self):
        return self.__class__(self.keyword, self.control, self.dur, self.kwargs)

    def reset(self):
        print("reset")

    @property
    def total_dur(self):
        return self.dur

    @property
    def averege_tempo(self):
        return Clock.bpm
