from FoxDot import MidiOut
from section_player import SectionPlayer
from FoxDot import Clock
from FoxDot import TimeVar
from FoxDot import Scale

class Control(object):

    def __init__(self, midinote, min, max, default_amp):
        self.min = min
        self.max = max
        self._value = self.scale(default_amp)
        self.midiout = MidiOut(channel = 15, oct = 0, degree = midinote, amp = self._value, scale = Scale.chromatic)
        self.is_playing = False

    def scale(self, val):
        return (val - self.min) / (self.max - self.min)

    def __call__(self, arg, dur = None):
        if self.is_playing:
            print("Control already playing")
            return
        self.player = SectionPlayer()
        self.is_playing = True
        val = self.scale(arg)
        self.player >> self.midiout
        self.player.amp = self.value

        if dur is not None:
            inc = (val - self.value) / dur
            Clock.future(1, self.set, kwargs = {"inc" : inc, "val" : val})
        elif isinstance(arg, TimeVar):
            self.player.amp = val
        else:
            self.value = val
            Clock.future(1, self.stop)


    def stop(self):
        self.player.stop()
        self.is_playing = False

    def set(self, inc, val):
        self.value = self.value + inc
        if (abs(self.value - val) < 0.01):
            self.value = val
            Clock.future(2, self.stop)
        else:
            Clock.future(1, self.set, kwargs = {"inc" : inc, "val" : val})

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        self._value = new_val
        self.player.amp = new_val
        self.midiout.amp = new_val

    def __invert__(self):
        self.stop()


class Tremolo(Control):

    def scale(self, val):
        if val == 1/64:
            return 2.0/127.0
        elif val == 1/32:
            return 10.0/127.0
        elif val == 1/24:
            return 20.0/127.0
        elif val == 1/16:
            return 25.0 / 127.0
        elif val == 1/12:
            return 30.0 / 127.0
        elif val == 1/8:
            return 35.0 / 127.0
        elif val == 1/6:
            return 40.0 / 127.0
        elif val == 3/16:
            return 45.0 / 127.0
        elif val == 1/4:
            return 50.0 / 127.0
        elif val == 5/16:
            return 55.0 / 127.0
        elif val == 1/3:
            return 60.0 / 127.0
        elif val == 3/8:
            return 65.0 / 127.0
        elif val == 1/2:
            return 75.0 / 127.0
        elif val == 3/4:
            return 80.0 / 127.0
        elif val == 1:
            return 85.0 / 127.0
        elif val == 3/2:
            return 90.0 / 127.0
        elif val == 2:
            return 95.0 / 127.0
        elif val == 3:
            return 100.0 / 127.0
        elif val == 4:
            return 105.0 / 127.0
        elif val == 6:
            return 110.0 / 127.0
        elif val == 8:
            return 115.0 / 127.0
        elif val == 16:
            return 120.0 / 127.0
        elif val == 32:
            return 1.0
        else:
            print("can't set lfo rate at", val)

class Wave(Control):

    def scale(self, val):
        if val == "sine":
            return 2.0 / 127.0
        elif val == "up":
            return 30.0 / 127.0
        elif val == "down":
            return 40.0 / 127.0
        elif val == "triangle":
            return 60.0 / 127.0
        elif val == "square":
            return 80.0 / 127.0
        elif val == "random":
            return 100.0 / 127.0
        else:
            print("no such wave", val)

class Mic(Control):

    def scale(self, val):
        if val == "on":
            return 127.0 / 127.0
        elif val == "off":
            return 10.0 / 127.0
        else:
            return("wrong input", val)

# implement wave etc.



# also some sections as

# toms, voices, drone

#time_begins()

#time_flies()

#time_fails()

#time_waits()

#time_trembles()

#time_runs_out()

#time_ends()

#and_begins_again()
