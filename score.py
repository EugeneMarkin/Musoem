from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from music21.meter.base import TimeSignature as M21TS
from music21.stream.base import PartStaff
from music21.instrument import Instrument
from measure import Measure
from measure import TimeSignature
from FoxDot import Pattern
from section import Section
from music21.tempo import MetronomeMark

# --- Structure: ------
# Voice contains Sections (which can be mapped to the FoxDot patterns)
# Section contains measures (which can also be mapped to FoxDot patterns)
# Both measures and sections contain patterns of pitch, offset, octave and duration

class Voice:

    def __init__(self, id, measures_list: [Measure]):
        self.id = id
        self._measures = measures_list

    def append(self, mes: Measure):
        self._measures.append(mes)

    def section(self, from_measure: int, to_measure: int) -> Section:
        return Section(self._measures[from_measure-1:to_measure])

    @property
    def all(self) -> Section:
        return Section(self._measures)

    @property
    def measures(self):
        return self._measures

class Part:

    def __init__(self, instrument, clef, partStaff: PartStaff, metro_marks, id):
        self.instrument = instrument
        self.clef = clef
        self._voices = {}
        self.id = id
        self.metro_marks = metro_marks
        for obj in partStaff.iter:
            if type(obj) == M21TS:
                # TODO: refactor the time signature stuff
                self.current_time_sig = TimeSignature.newFromM21TS(obj)
            elif type(obj) == M21Measure:
                self._parse_measure(obj, obj.number)

    def _parse_measure(self, m21_measure, index):
        if m21_measure.hasVoices():
            for v in m21_measure.voices:
                vid = int(v.id)
                measure = self._createMeasure(index, m21_measure, vid)
                if vid not in self._voices:
                    voice = Voice(vid, [measure])
                    self._voices[vid] = voice
                else:
                    self._voices[vid].append(measure)
        else:
            measure = self._createMeasure(index, m21_measure, -1)
            if -1 not in self._voices:
                self._voices[-1] = Voice(-1, [measure])
            else:
                self._voices[-1].append(measure)

    def _createMeasure(self, id, m21_measure, vid) -> Measure:
        mes_start = m21_measure.offset
        mes_end = mes_start + m21_measure.duration.quarterLength
        for (start, end, mm) in self.metro_marks:
            if mes_start >= start and mes_end <= end:
                self.bpm = self._get_bpm_from_metronome_mark(mm)
                break
        # multiple metro marks per measure are not supported for now
        if m21_measure.timeSignature is not None:
            self.current_time_sig = TimeSignature.newFromM21TS(m21_measure.timeSignature)

        measure = Measure(id, m21_measure, self.current_time_sig, self.bpm, vid)
        # we update these properties because there might be tempo and meter
        # changes within the measure itself.
        # As per common notation rules meter and tempo changes affect all
        # the subsequent score until next mark
        self.current_time_sig = measure.timeSignature
        return measure

    def _get_bpm_from_metronome_mark(self, mm):
        num = float(mm.number)
        dur = float(mm.referent.quarterLength)
        return num / dur

    @property
    def voices(self):
        return self._voices


class Score(Voice):

    def __init__(self, sc: M21Score):
        # lines notated on different staves are parsed as separate parts
        parts = sc.parts
        self._parts = {}
        self.bpm = 120
        # current time signature (last notated)
        self.current_time_sig = TimeSignature(4, 4)

        # todo handle metronome marks properly
        metro_marks = sc.metronomeMarkBoundaries()

        print("parts in score:", len(parts))

        for partStaff in parts:
            instr = partStaff.getInstrument(returnDefault=False).instrumentName
            clef = self._get_clef_from_partStaff(partStaff)
            part_id = instr + "_" + clef
            part = Part(instr, clef, partStaff, metro_marks, part_id)
            self._parts[part_id] = part
    #def _get_bpm_list_for_measure(index):

    def _get_clef_from_partStaff(self, partStaff):
        for obj in partStaff.elements:
            if type(obj) == M21Measure:
                clef = obj.clef.name
                break
        return clef

    @property
    def parts(self):
        return self._parts

    def section(self, from_measure: int, to_measure: int,  instrument, voice = -1, clef = "treble") -> Section:
        partKey = [instrument + "_" + clef]
        if not partKey in self._parts.keys():
            print("Warning: no part for ", instrument, " and ", clef)
            return None
        part = self._parts[partKey]
        if not voice in part.voices:
            print("Warning: no voice number found:", voice)
            return None
        voice_part = part.voices[voice]
        # TODO: add empty measures for voices
        return voice_part.section(from_measure, to_measure)

    @property
    def all(self):
        res = {}
        for part in self._parts.values():
            for voice in part.voices.values():
                key = part.id + " voice: " + str(voice.id)
                res[key] = voice.all
        return res
