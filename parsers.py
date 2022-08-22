from music21.stream import Stream
from music21.stream.base import Measure as M21Measure
from music21.stream.base import PartStaff
from music21.stream.base import Score
from music21.scale import ChromaticScale
from music21.chord import Chord
from music21.note import Note, Rest, GeneralNote, Unpitched
from music21.stream.iterator import StreamIterator
from music21.tempo import MetronomeMark
from time_signature import TimeSignature
from music21.meter.base import TimeSignature as M21TS

# This class parses the music21 tree of a score



    # Assumed structure is:
    #             Score
    #          /        \
    #     PartStaff     PartStaff
    #     /      \              \
    #   Measure  Measure         Measure -> Voice
    #  /    |  \                                 \
    # (Note, Rest, TimeSignature, MetronomeMark) (Note, Rest, TimeSignature, MetronomeMark, ...)

# NOTE: the assumed structure is tested with a MusicXML file exported from Sibelius
# Other software might theoretially build a different tree structure, e.g.
# put TimeSignature or MetronomeMark objects at a different level of the hierarchy,
# which may cause this parser to fail
# TODO: write intergration tests with a number of different MusicXML files

# The TimeSignature object is expected to be found at PartStaff level
# MetronomeMark objects are found on note level withing measures
# We want each voice of each measure to know its time and tempo, so we pass
# previously found metro marks and time signatures further up the tree when parsing

class ScoreParser:

    def __init__(self, score: Score):
        self.parts = {}
        prev_part = None
        for partStaff in score.parts:
            part_staff_parser = PartStaffParser(partStaff, prev_part)
            prev_part = part_staff_parser
            part_id = part_staff_parser.id
            self.parts[part_id] = part_staff_parser

class PartStaffParser:

    def __init__(self, partStaff: PartStaff, prev_part):
        self.instrument = partStaff.getInstrument(returnDefault=False).instrumentName
        self.clef = self._get_clef_from_partStaff(partStaff)
        self.id = partStaff.id
        self.measures = []
        measure_index = 0
        for obj in partStaff.iter:
            ts = None
            if type(obj) == M21TS:
                # TODO: refactor the time signature stuff
                ts = TimeSignature.newFromM21TS(obj)
            elif type(obj) == M21Measure:
                if measure_index == 0:
                    if prev_part is not None:
                        top_measure = prev_part.measures[0]
                        prev_bpm = top_measure.bpm
                    else:
                        prev_bpm = []
                    mp = MeasureParser(obj, ts, prev_bpm)
                else:
                    prev_ts = self.measures[measure_index-1].ts
                    if prev_part is not None:
                        prev_bpm = prev_part.measures[measure_index].bpm
                    else:
                        prev_bpm = self.measures[measure_index-1].bpm
                        if len(prev_bpm) > 1:
                            prev_bpm = [prev_bpm[-1]]
                    mp = MeasureParser(obj, prev_ts, prev_bpm)
                self.measures.append(mp)
                measure_index+=1

    def _get_clef_from_partStaff(self, partStaff):
        for obj in partStaff.elements:
            if type(obj) == M21Measure:
                clef = obj.clef.name
                break
        return clef

class MeasureParser:

    def __init__(self, measure: M21Measure, prev_ts, prev_bpm):
        #voice = list(filter(lambda v: int(v.id) == voiceN, measure.voices))[0]
        self.id = measure.number
        self._parse_time_signature(measure, prev_ts)
        self.voices = {}
        self.bpm = prev_bpm.copy()

        if measure.hasVoices():
            for voice in measure.voices:
                vp = VoiceParser(voice, prev_bpm)
                prev_bpm = vp.bpm
                self.voices[voice.id] = vp
        else:
            vp = VoiceParser(measure, prev_bpm)
            self.bpm = vp.bpm
            self.voices["-1"] = vp
        # all voices in the measure should have the same bpm anyway

    def _parse_time_signature(self, measure, prev_ts):
        # multiple metro marks per measure are not supported for now
        if measure.timeSignature is not None:
            self.ts = TimeSignature.newFromM21TS(measure.timeSignature)
        else:
            self.ts = prev_ts

class VoiceParser:

    def __init__(self, stream, prev_bpm):
        self.pitch = []
        self.octave = []
        self.duration = []
        self.bpm = prev_bpm.copy()
        for element in stream.iter:
            self._parse_element(element)

    def _parse_element(self, element):

        if (not type(element) == Note
            and not type(element) == Rest
            and not type(element) == Chord
            and not type(element) == Unpitched
            and not type(element) == MetronomeMark):
            #    print("This is not implemented: ", type(element))
                return

        if type(element) == Note:
            self._parse_note(element)
        elif type(element) == Rest:
            self._parse_rest(element)
        elif type(element) == Chord:
            self._parse_chord(element)
        elif isinstance(element, Unpitched):
            self._parse_unpitched(element)
        elif isinstance(element, MetronomeMark):
            self._parse_metro_mark(element)


    def _parse_note(self, note):
        degree = self._get_scale_degree(note.pitch)
        dur = note.quarterLength
        if degree is None:
            print("faulty element ", note)
        if note.tie is not None:
            if note.tie.type == 'start':
                dur = self._get_note_duration(note)
            else:
                self.pitch.append('rest')
                self.octave.append('rest')
                self.duration.append(dur)
                return
        oct = note.octave
        self.pitch.append(degree)
        self.octave.append(oct)
        self.duration.append(dur)


    def _parse_chord(self, chord):
        note = chord.notes[0]
        dur = chord.quarterLength
        if note.tie is not None:
            if note.tie.type == 'start':
                dur = self._get_chord_duration(chord)
            else:
                self.pitch.append('rest')
                self.octave.append('rest')
                self.duration.append(dur)
                return
        p_map = map(lambda p: self._get_scale_degree(p), chord.pitches)
        o_map = map(lambda n: n.octave, chord.notes)
        self.pitch.append(list(p_map))
        self.octave.append(list(o_map))
        self.duration.append(dur)

    def _parse_rest(self, rest):
        self.pitch.append('rest')
        self.octave.append('rest')
        self.duration.append(rest.quarterLength)

    def _parse_unpitched(self, unpitched):
        self.pitch.append("unpitched")
        self.octave.append("unpitched")
        self.duration.append(unpitched.quarterLength)

    def _parse_metro_mark(self, mm):
        print("parse metro mark", mm)
        self.bpm.append(self._get_bpm_from_metronome_mark(mm))
    # if has a tie of type 'start' we need to find the end
    # of the tie and adjust the note's duration.
    # the resulting duration may exceed the duration of the measure,
    # but that is ok in our case
    def _get_note_duration(self, note) -> float:
        note_pitch = note.pitch
        note_octave = note.octave
        note_dur = note.quarterLength
        next = note.next()
        while next is not None:
            if (isinstance(next, Note)
             and next.pitch == note_pitch
             and next.octave == note_octave):
                if next.tie is not None:
                    if next.tie.type != 'start':
                        note_dur += next.quarterLength
                    if next.tie.type == 'stop':
                        break
            next = next.next()
        return note_dur

    def _get_chord_duration(self, chord) -> float:
        chord_pitches = chord.pitches
        chord_octaves = list(map(lambda n: n.octave, chord.notes))
        chord_dur = chord.quarterLength
        next = chord.next()
        while next is not None:
            if (isinstance(next, Chord) and
                next.pitches == chord_pitches and
                (list(map(lambda n: n.octave, chord.notes))) == chord_octaves):
                    note = next.notes[0]
                    if note.tie.type != 'start':
                        chord_dur += note.quarterLength
                    if note.tie.type == 'stop':
                        break
            next = next.next()
        return chord_dur

    def _get_scale_degree(self, pitch):
        # always use C chromatic scale for now
        scale = ChromaticScale('C')
        # scale degrees in FoxDot scales start from 0, thus -1
        return scale.getScaleDegreeFromPitch(pitch, comparisonAttribute='pitchClass') - 1

    def _get_bpm_from_metronome_mark(self, mm) -> float:
        num = float(mm.number)
        dur = float(mm.referent.quarterLength)
        return num / dur
