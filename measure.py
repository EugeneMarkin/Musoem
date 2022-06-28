from music21.stream.base import Measure as M21Measure
from music21.key import KeySignature
from music21.scale import ChromaticScale
from music21.chord import Chord
from music21.note import Note, Rest
from music21.meter.base import TimeSignature as M21TS
from music21.stream.iterator import StreamIterator
from music21.tempo import MetronomeMark
from music21.tempo import TempoIndication

from FoxDot import rest
from FoxDot import Pattern
from FoxDot import PGroup

class TimeSignature:

    def __init__(self, num, dur):
        self.values = (num, dur)

    @classmethod
    def newFromM21TS(cls, ts: M21TS):
        num = int(ts.beatCount)
        dur = int(4 * float(ts.beatDuration.quarterLength))
        return TimeSignature(num, dur)

    def asTuple(self):
        return self.values

    def numerator(self):
        return self.values[0]

    def denominator(self):
        return self.values[1]


class BPM:
    def __init__(self, val):
        self.val= val

    @classmethod
    def bpmFromMetronomeMark(cls, mm: MetronomeMark):
        num = float(mm.number)
        dur = float(mm.referent.quarterLength)
        self.val = num / dur

    @property
    def value(self):
        return self.val

class Measure:

    # if we dont want to extract an individual voice, we can skip the last arg
    def __init__(self,
                 idx: int,
                 mes: M21Measure,
                 ts,
                 bpm,
                 voiceN = -1) -> TimeSignature:
        self.idx: int = idx # the original place of the measure in score (for reference)
        self.timeSignature = ts
        mts = mes.timeSignature
        if mts is not None:
            self.timeSignature = TimeSignature.newFromM21TS(mts)
        self.pitch = Pattern([])
        self.octave = Pattern([])
        self.duration = Pattern([])
        self.offset = Pattern([])
        self.bpm = bpm

        # key = mes.keySignature.asKey

        if voiceN == -1:
            self._parse_notes_and_rests(mes.notesAndRests)
        else:
            voice = list(filter(lambda v: int(v.id) == voiceN, mes.voices))[0]
            self._parse_notes_and_rests(voice.notesAndRests)

    def _parse_notes_and_rests(self, iter: StreamIterator):
        # always use C chromatic scale for now
        scale = ChromaticScale('C')
        for element in iter:
            if isinstance(element, Note):
                # scale degrees in FoxDot scales start from 0, thus -1
                degree = scale.getScaleDegreeFromPitch(element.pitch) - 1
                oct = element.octave
                self.pitch.extend([degree])
                self.octave.extend([oct])
            elif isinstance(element, Rest):
                # add some pitch for rest to keep pattern length consistent
                # TODO: special symbol for rest pitch?
                self.pitch.append([0])
                self.octave.extend([5])
            elif isinstance(element, Chord):
                p_map = map(lambda p: scale.getScaleDegreeFromPitch(p) - 1, element.pitches)
                group = PGroup(list(p_map))
                self.pitch.extend([group])
                o_map = map(lambda n: n.octave, element.notes)
            elif isinstance(element, MetronomeMark):
                print("Found metronome mark inside the measure")
                self.bpm = BPM.bpmFromMetronomeMark(element)
            elif isinstance(element, TempoIndication):
                print("Found tempo text")
            else:
                print("This is not implemented: ", type(element))

            off = element.offset # within the measure
            dur_q = element.quarterLength

    @property
    def description(self):
        desc = "Measure " + str(self.idx)
        desc += "," + "Time sig. " + str(self.timeSignature.asTuple())
        desc += "bpm: " + str(self.bpm.value)
        return desc
