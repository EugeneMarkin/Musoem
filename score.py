from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from music21.stream.base import PartStaff
from music21.instrument import Instrument
from measure import Measure
from time_signature import TimeSignature
from FoxDot import Pattern
from section import Section
from music21.tempo import MetronomeMark
from parsers import ScoreParser
from part import Part

# A class representing an entire score
# Score consists of parts - single staff part in the MusicXML score
# Part can have single or multiple voices (as in music engraving software)

class Score:

    # TODO: add a class method constructor to create Score from a file path
    # Parse from music21 Score object
    def __init__(self, sc: M21Score, instr_map = None):
        # lines notated on different staves are parsed as separate parts
        self._parts = {}
        self._instr_map = instr_map
        score_parser = ScoreParser(sc)
        for part_id in score_parser.parts:
            part_staff_parser = score_parser.parts[part_id]
            part = Part(part_staff_parser)
            self._parts[part_id] = part

    @property
    def parts(self):
        return self._parts

        # Extract a section of the score that contains a range of measures for a single insturment and clef
        # Note: only 1 voice can be contained in a section. Default voice will be used if argument is omitted
    def section(self, from_measure:int, to_measure: int, part_key, voice = "-1") -> Section:
        if not part_key in list(self._parts.keys()):
            print("Warning: no part for ", part_key)
            return None
        else:
            part = self._parts[part_key]
            if not voice in part.voices:
                print("Warning: no voice number found:", voice)
            else:
                voice_part = part.voices[voice]

        instrument_key = self._get_instrument_for_key(part_key, voice)
        section = voice_part.section(from_measure, to_measure, instrument_key)
        print(section.description)
        return section

    def _get_instrument_for_key(self, part_key, voice):
        if self._instr_map is None:
            return None
        if part_key in self._instr_map:
            instr_data = self._instr_map[part_key]
            if isinstance(instr_data, dict):
                if voice not in instr_data:
                    return None
                else:
                    return instr_data[voice]
            elif isinstance(instr_data, str):
                return instr_data

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
