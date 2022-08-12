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


# A class representing an entire score
# Score consists of parts - single staff part in the MusicXML score
# Part can have single or multiple voices (as in music engraving software)

class Score:

    # TODO: add a class method constructor to create Score from a file path
    # Parse from music21 Score object
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

    # Extracts the clef given a partStaff (music21) object
    def _get_clef_from_partStaff(self, partStaff):
        for obj in partStaff.elements:
            if type(obj) == M21Measure:
                clef = obj.clef.name
                break
        return clef

    @property
    def parts(self):
        return self._parts

    # Extract a section of the score that contains a range of measures for a single insturment and clef
    # Note: only 1 voice can be contained in a section. Default voice will be used if argument is omitted
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

    # Returns a dictionary where keys are individual parts or part voices
    # and values are Section objects containing ALL measures of the score
    @property
    def all(self):
        res = {}
        for part in self._parts.values():
            for voice in part.voices.values():
                key = part.id + " voice: " + str(voice.id)
                res[key] = voice.all
        return res
