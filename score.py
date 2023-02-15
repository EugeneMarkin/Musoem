from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from music21.stream import PartStaff
from music21.instrument import Instrument
from measure import Measure
from time_signature import TimeSignature
from FoxDot import Pattern, Server
from section import Section
from sample import Sample, SampleList
from music21.tempo import MetronomeMark
from parsers import ScoreParser, MidiParser
from part import Part
import os

# A class representing an entire score coming from a single MusicXML file
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

    @property
    def sections(self):
        res = []
        for key, part in self._parts.items():
            for tm in part.text_marks:
                m_start = tm.measure_num
                m_end = m_start + tm.length - 1
                section = self.section(m_start, m_end, key)
                section.keyword = tm.text
                res.append(section)
        return res

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


# TODO: make proper file heierarchy
class FileScore(Score):

    def __init__(self, folder_path, bpm):
        self.bpm = bpm
        # TODO: rename this to playables
        self.sections = {}
        self.buf_num_generator = BufNumGenerator()
        dir = os.listdir(folder_path)
        for instrument in dir:
            # skip system files
            if instrument[0] == ".":
                continue
            if not os.path.isdir(folder_path + "/" + instrument):
                continue
            instrument_path = folder_path + "/" + instrument
            instrument_dir = os.listdir(instrument_path)
            if "midi" in instrument:
                self.sections.update(self.load_midi_files(instrument_dir, instrument, instrument_path))
            elif "sample" in instrument:
                self.sections.update(self.load_audio_files(instrument_dir, instrument, instrument_path))

    def load_midi_files(self, files, instrument, path):
        result = {}
        for file in files:
            kw = os.path.splitext(file)[0]
            if ".mid" in file:
                section = self.midi_section(path + "/" + file, instrument, kw)
                result[kw] = section
            elif os.path.isdir(path + "/" + file):
                files = sorted(os.listdir(path + "/" + file))
                midi_set = self.load_midi_files(files, instrument, path + "/" + file).values()
                midi_set = SectionList(list(midi_set))
                for s in midi_set: s.keyword = kw
                result[kw] = midi_set
        return result

    def midi_section(self, file, instrument, keyword):
        mp = MidiParser(file)
        measure = Measure(1, mp.pitch, mp.octave, mp.duration, mp.sus, mp.amp, self.bpm, TimeSignature(4,4))
        return Section([measure], instrument, keyword)


    def load_audio_files(self, files, instrument, path):
        result = {}
        for file in files:
            kw = os.path.splitext(file)[0]
            if ".wav" in file or ".aif" in file or ".aiff" in file:
                bufnum = self.buf_num_generator.next
                Server.bufferRead(path + "/" + file, bufnum)
                sample = Sample(kw, instrument, bufnum)
                result[kw] = sample
                bufnum += 1
            # if the instrument directory contains subdirectories
            # we interpret it as a set of files that should be assigned to the same keyword
            elif os.path.isdir(path + "/" + file):
                    files = sorted(os.listdir(path + "/" + file))
                    sample_set = self.load_audio_files(files, instrument, path + "/" + file).values()
                    sample_set = list(sample_set)
                    if len(sample_set) > 1:
                        buffers = list(map(lambda x: x.bufnum, sample_set))
                        print(buffers)
                        sample_set = SampleList(kw, instrument, buffers)
                        for s in sample_set: s.keyword = kw
                        result[kw] = sample_set
                    else:
                        result[kw] = sample_set[0]
        return result

    def __getitem__(self, key):
        return self.sections[key]

class BufNumGenerator:

    def __init__(self):
        self.bufnum = 0

    @property
    def next(self):
        self.bufnum += 1
        return self.bufnum

# TODO: move this class somewhere else
class SectionList:

    def __init__(self, list):
        self.list = list
        self.index = 0

    @property
    def next(self):
        res = self.list[self.index]
        if self.index < len(self.list) - 1:
            self.index += 1
        else:
            self.index = 0
        return res

    def __iter__(self):
        return iter(self.list)
