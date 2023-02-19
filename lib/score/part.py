# A class representing a part in the score.

# This definition of part assumes it has a single staff, e.g.
# Piano treble is one part, Piano bass is another part

# A Part contains the info of its instrument, clef, id, and metronome marks
# The actual measures containing notes belong to Voice class

# A Part either has once voice (default = -1) or can have multiple voices,
# in case of polyphonic texture for example.
from parsers import PartStaffParser
from parsers import MeasureParser
from voice import Voice
from measure import Measure

class Part:

    def __init__(self, psp: PartStaffParser):
        self.text_marks = psp.text_marks
        self.instrument = psp.instrument
        self.clef = psp.clef
        self._voices = {}
        self.id = psp.id
        for mp in psp.measures:
            self._createMeasure(mp)

    def _createMeasure(self, mp: MeasureParser):
        voices = mp.voices
        for voice_key in voices:
            vp = voices[voice_key]
            pitch = vp.pitch
            octave = vp.octave
            duration = vp.duration
            sustain = vp.sus
            amp = vp.amp
            bpm = mp.bpm
            ts = mp.ts
            id = mp.id
            measure = Measure(id, pitch, octave, duration, sustain, amp, bpm, ts)
            if voice_key not in self._voices:
                voice = Voice(voice_key, [measure])
                self._voices[voice_key] = voice
            else:
                self._voices[voice_key].append(measure)

    @property
    def measures(self) -> [Measure]:
        if len(self._voices) > 1:
            print("WARNING: part has multiple voices. Returning default voice")
        return self._voices[list(self._voices.keys())[0]].measures

    @property
    def voices(self) -> [Voice]:
        return self._voices
