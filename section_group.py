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
            dur = max(list(map(lambda x: x._get_clock_beats(x.total_dur), self._sections)))
            Clock.future(times * dur, self.stop)
        else:
            # TODO: simplify this by adding a function that returns total clock beats
            all_times = list(map(lambda x: x._times, self._sections))
            all_durs = list(map(lambda x: x._get_clock_beats(x.total_dur), self._sections))
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
