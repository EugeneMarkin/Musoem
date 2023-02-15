from FoxDot import rest
from FoxDot import Pattern
from FoxDot import PGroup

# A class representing a single measure of music for
# a single part and a single voice.
# Measure is a collection of FoxDot patterns that can be used in live coding

# If a measure contains a note that is ties to a note in the next measure,
# the note's duration will exceed the duration of the measure.

# If a measure contains a note that is tied to a note in previous measure,
# the note will be parsed as a rest.

class Measure:

    # if we dont want to extract an individual voice, we can skip the last arg
    def __init__(self,
                 index: int,
                 pitch,
                 octave,
                 duration,
                 sustain,
                 amp,
                 bpm,
                 ts):
        self.index = index # the original place of the measure in score (for reference)
        self.ts = ts
        self.bpm = Pattern(bpm)
        self._parse_lists_into_patterns(pitch, octave, duration, sustain, amp, bpm)


    def _parse_lists_into_patterns(self, pitch, octave, dur, sus, amp, bpm):
        self.degree = Pattern([])
        self.oct = Pattern([])
        self.dur = Pattern([])
        self.sus = Pattern([])
        self.amp = Pattern([])
        # TODO: refactor this to use append not extend
        measure_dur = self.ts.numerator * (4 / self.ts.denominator)
        for i, p in enumerate(pitch):
            if (p == 'unpitched' or p == 'rest'):
                self.degree.extend([0])
                self.oct.extend([5])
                if p == 'unpitched':
                    self.dur.extend([dur[i]])
                    self.sus.extend([sus[i]])
                    self.amp.extend([amp[i]])
                elif p == 'rest':
                    self.dur.extend([rest(dur[i])])
                    self.sus.extend([0])
            else:
                if type(p) is tuple:
                    self.degree.extend([PGroup(p)])
                    self.oct.extend([PGroup(octave[i])])
                else:
                    self.degree.extend([p])
                    self.oct.extend([octave[i]])
                self.dur.extend([dur[i]])
                self.sus.extend([sus[i]])
                self.amp.extend([amp[i]])


    @property
    def description(self):
        desc = "Measure " + str(self.index) + ", "
        desc += "bpm: " + str(self.bpm) + ", "
        desc += "time signature: " + self.ts.asString() + ", "
        desc += "degree: " + str(self.degree) + ", "
        desc += "octave: " + str(self.oct) + ", "
        desc += "duration: " + str(self.dur) + ", "
        desc += "sustain: " + str(self.sus)
        return desc
