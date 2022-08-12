from music21.stream.base import Measure as M21Measure
from music21.key import KeySignature
from music21.scale import ChromaticScale
from music21.chord import Chord
from music21.note import Note, Rest, GeneralNote, Unpitched
from music21.meter.base import TimeSignature as M21TS
from music21.stream.iterator import StreamIterator
from music21.tempo import MetronomeMark
from music21.tempo import TempoIndication
from music21.tie import Tie

from FoxDot import rest
from FoxDot import Pattern
from FoxDot import PGroup

# A class representing a single measure of music for
# a single part and a single voice.

# If a measure contains a note that is ties to a note in the next measure,
# the note's duration will exceed the duration of the measure.

# If a measure contains a note that is tied to a note in previous measure,
# the note will be parsed as a rest.

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
        self.pitch = Pattern([])
        self.octave = Pattern([])
        self.duration = Pattern([])
        self.bpm = bpm
        self.voiceNum = voiceN

        # key = mes.keySignature.asKey

        if voiceN == -1:
            self._parse_notes_and_rests(mes.notesAndRests)
        else:
            voice = list(filter(lambda v: int(v.id) == voiceN, mes.voices))[0]
            self._parse_notes_and_rests(voice.notesAndRests)

    def _parse_notes_and_rests(self, iter: StreamIterator):
        # always use C chromatic scale for now

        for element in iter:
            if (not type(element) == Note
                and not type(element) == Rest
                and not type(element) == Chord):
                    print("This is not implemented: ", type(element))
                    continue
            dur = element.quarterLength

            if type(element) == Note:
                # scale degrees in FoxDot scales start from 0, thus -1
                degree = self._get_scale_degree(element.pitch)
                if degree is None:
                    print("faulty element ", element)
                oct = element.octave
                self.pitch.extend([degree])
                self.octave.extend([oct])
                self.duration.extend([dur])

            elif type(element) == Rest:
                # add some pitch for rest to keep pattern length consistent
                # TODO: special symbol for rest pitch?
                self.pitch.extend([0])
                self.octave.extend([5])
                self.duration.extend([rest(dur)])

            elif type(element) == Chord:
                p_map = map(lambda p: self._get_scale_degree(p), element.pitches)
                o_map = map(lambda n: n.octave, element.notes)
                self.pitch.extend([PGroup(list(p_map))])
                self.octave.extend([PGroup(list(o_map))])
                self.duration.extend([dur])

            elif type(element) == Tie:
                print("found a tie of type ", element.type)
            elif isinstance(element, Unpitched):
                print("unpitched")

    def _get_scale_degree(self, pitch):
        scale = ChromaticScale('C')
        return scale.getScaleDegreeFromPitch(pitch, comparisonAttribute='pitchClass') - 1
    @property
    def description(self):
        desc = "Measure " + str(self.idx) + ", "
        desc += "Voice: " + str(self.voiceNump)
        desc += ", " + "Time sig. " + str(self.timeSignature.asTuple())
        desc += "bpm: " + str(self.bpm) + ", "
        desc += "pitch: " + str(self.pitch) + ", "
        desc += "octave: " + str(self.octave) + ", "
        desc += "duration: " + str(self.duration) + ", "
        return desc
