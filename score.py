from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from music21.meter.base import TimeSignature as M21TS
from measure import Measure
from measure import TimeSignature
from FoxDot import Pattern
from section import Section
from measure import BPM
from music21.tempo import MetronomeMark

# --- Structure: ------
# Score is either itself a voice or contains multiple voices
# Voice contains Sections (which can be mapped to the FoxDot patterns)
# Section contains measures (which can also be mapped to FoxDot patterns)
# Both measures and sections contain patterns of pitch, offset, octave and duration

class Voice:

    def __init__(self, measures_list: [Measure] = []):
        self._measures = measures_list

    def append(self, mes: Measure):
        self._measures.append(mes)

    def section(self, fr: int, to: int) -> Section:
        return Section(self._measures[fr:to])

    def all(self) -> Section:
        return Section(self._measures)

    @property
    def measures(self):
        return self._measures

class Score(Voice):

    def __init__(self, sc: M21Score):
        # lines notated on different staves are parsed as separate parts
        parts = sc.parts
        self._voices = {}
        # current time signature (last notated)
        self.current_time_sig = TimeSignature(4, 4)
        self.bpm = BPM(120)
        print("parts in score:", len(parts))

        for i, part in enumerate(parts):
            self._parsePart(part, i)

    def _parsePart(self, part, part_num):
        print("parsing part", part)
        new_voice = Voice()
        default_key = "default" + str(part_num)
        self._voices[default_key] = new_voice

        for i, obj in enumerate(part.elements):
            if type(obj) == M21TS:
                self.current_time_sig = TimeSignature.newFromM21TS(obj)
            elif type(obj) == MetronomeMark:
                print("found metro mark")
                self.bpm = BPM.bpmFromMetronomeMark(obj)
            elif type(obj) == M21Measure:
                self._parse_measure(obj, i, default_key)


    def _parse_measure(self, m21_measure, index, voice_key):
            if m21_measure.hasVoices():
                for v in m21_measure.voices:
                    vid = int(v.id)
                    measure = self._createMeasure(index, m21_measure, vid)
                    if vid not in self._voices:
                        voice = Voice([measure])
                        self._voices[vid] = voice
                    else:
                        self._voices[vid].append(measure)
            else:
                measure = self._createMeasure(index, m21_measure, -1)
                self._voices[voice_key].append(measure)

    def _createMeasure(self, id, m21_measure, vid) -> Measure:
        measure = Measure(id, m21_measure, self.current_time_sig, self.bpm, vid)
        # we update these properties because there might be tempo and meter
        # changes within the measure itself.
        # As per common notation rules meter and tempo changes affect all
        # the subsequent score until next mark
        self.current_time_sig = measure.timeSignature
        self.bpm = measure.bpm
        return measure

    @property
    def voices(self):
        return list(self._voices.values())

    def section(self, fr: int, to: int) -> Section:
        return self._voices[0].section(fr, to)

    def all(self) -> Section:
        return self._voices[0].all()

    def numVoices(self):
        return len(self._voices)
