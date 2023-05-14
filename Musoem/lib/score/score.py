import os
from music21.stream import Score as M21Score
from music21.stream import Measure as M21Measure
from music21.stream import PartStaff
from music21.tempo import MetronomeMark
from music21 import converter
from FoxDot import Pattern, Server

from .measure import Measure
from .time_signature import TimeSignature

from ..playables.section import Section, SectionList
from ..playables.sample import Sample, SampleList
from ..player.instrument import Instrument
from ..util.utils import get_bpm_from_path

from ..parsers.parsers import ScoreParser, MidiParser
from .part import Part


# A class representing an entire score coming from a single MusicXML file
# Score consists of parts - single staff part in the MusicXML score
# Part can have single or multiple voices (as in music engraving software)

class Score:

    @property
    def playables(self):
        # Override me
        return None

class MusicXMLScore(Score):

    # TODO: add a class method constructor to create Score from a file path
    # Parse from music21 Score object
    def __init__(self, path):
        # lines notated on different staves are parsed as separate parts
        m21score = converter.parse(path, format = "musicxml")
        self._parts = {}
        score_parser = ScoreParser(m21score)
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

        section = voice_part.section(from_measure, to_measure)
        return section

    @property
    def playables(self):
        res = []
        for key, part in self._parts.items():
            for tm in part.text_marks:
                m_start = tm.measure_num
                m_end = m_start + tm.length - 1
                section = self.section(m_start, m_end, key)
                section.keyword = tm.text
                res.append(section)
        return res

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



# This class assembles a score out of midi and/or audio files contained in a dir
class FileScore(Score):

    def __init__(self, folder_path):
        # TODO: rename this to playables
        self._playables = {}
        self.buf_num_generator = BufNumGenerator()
        dir = os.listdir(folder_path)
        for instr in dir:
            # skip system files
            instrument_path = folder_path + "/" + instr
            if instr[0] == ".":
                continue
            if not os.path.isdir(instrument_path):
                continue
            instrument_dir = os.listdir(instrument_path)
            if instr in Instrument.sampler_synths(): # TODO: change this
                self._playables.update(self.load_audio_files(instrument_dir, Instrument(instr), instrument_path))
            elif instr in Instrument.all_synths() or "midi" in instr:
                self._playables.update(self.load_midi_files(instrument_dir, Instrument(instr), instrument_path))
            else:
                print("WARNING: no instrument with name ", instr)
            any_bpm = get_bpm_from_path(instrument_path)
            for p in self._playables.values():
                if p.bpm == None or p.bpm == Pattern([]) :
                    p.bpm = Pattern([any_bpm])

    def load_midi_files(self, files, instrument, path):
        print("load midi files")
        result = {}
        for file in files:
            kw = os.path.splitext(file)[0]
            if ".mid" in file:
                section = self.midi_section(path + "/" + file, instrument, kw)
                result[kw] = section
            elif os.path.isdir(path + "/" + file):
                files = sorted(os.listdir(path + "/" + file))
                midi_set = self.load_midi_files(files, instrument, path + "/" + file).values()
                midi_set = SectionList(instrument, kw, list(midi_set))
                for s in midi_set: s.keyword = kw
                result[kw] = midi_set
        return result

    def midi_section(self, file, instrument, keyword):
        mp = MidiParser(file)
        measure = Measure(1, mp.pitch, mp.octave, mp.duration, mp.sus, mp.amp, [], TimeSignature(4,4))
        return Section([measure], instrument, keyword)


    def load_audio_files(self, files, instrument, path):
        result = {}
        for file in files:
            kw = os.path.splitext(file)[0]
            if ".wav" in file or ".aif" in file or ".aiff" in file:
                bufnum = self.buf_num_generator.next
                #print(kw," bufnum ", bufnum)
                Server.bufferRead(path + "/" + file, bufnum)
                sample = Sample(instrument, kw, bufnum)
                result[kw] = sample
                bufnum += 1
            # if the instrument directory contains subdirectories
            # we interpret it as a set of files that should be assigned to the same keyword
            elif os.path.isdir(path + "/" + file):
                    files = sorted(os.listdir(path + "/" + file))
                    sample_set = self.load_audio_files(files, instrument, path + "/" + file).values()
                    sample_set = list(sample_set)
                    if len(sample_set) >= 1:
                        buffers = list(map(lambda x: x.buf.data[0], sample_set))
                        sample_set = SampleList(instrument, kw , buffers)
                        for s in sample_set: s.keyword = kw
                        result[kw] = sample_set
                    else:
                        result[kw] = sample_set[0]
        return result

    def __getitem__(self, key):
        return self._playables[key]

    @property
    def playables(self):
        return self._playables.values()


class BufNumGenerator:

    def __init__(self):
        self.bufnum = 0

    @property
    def next(self):
        self.bufnum += 1
        return self.bufnum
