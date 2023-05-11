from music21.stream import Stream
from music21.stream.base import Measure as M21Measure
from music21.stream.base import PartStaff, Part
from music21.stream.base import Score
from music21.scale import ChromaticScale
from music21.chord import Chord
from music21.note import Note, Rest, GeneralNote, Unpitched
from music21.stream.iterator import StreamIterator
from music21.tempo import MetronomeMark
from music21.expressions import TextExpression
from music21.meter.base import TimeSignature as M21TS
from music21.converter import parse as parse_midi
from music21.bar import Barline

from ..score.text_mark import TextMark
from ..score.time_signature import TimeSignature
from ..base.constants import TRIM_MIDI_CLIPS


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

    def __init__(self, partStaff: Part, prev_part):

        self.instrument = partStaff.partName.lower()
        self.clef = self._get_clef_from_partStaff(partStaff)
        self.id = partStaff.id
        self.measures = []
        self.text_marks = []
        measure_index = 0
        for obj in partStaff:
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
                    mp = MeasureParser(obj, ts, prev_bpm, partStaff)
                else:
                    prev_ts = self.measures[measure_index-1].ts
                    if prev_part is not None:
                        prev_bpm = prev_part.measures[measure_index].bpm
                    else:
                        prev_bpm = self.measures[measure_index-1].bpm
                        if len(prev_bpm) > 1:
                            prev_bpm = [prev_bpm[-1]]
                    mp = MeasureParser(obj, prev_ts, prev_bpm, partStaff)
                self.measures.append(mp)
                self.text_marks.extend(mp.text_marks)
                measure_index+=1

    def _get_clef_from_partStaff(self, partStaff):
        for obj in partStaff.elements:
            if type(obj) == M21Measure:
                clef = obj.clef.name
                break
        return clef

class MeasureParser:

    def __init__(self, measure: M21Measure, prev_ts, prev_bpm, part):
        #voice = list(filter(lambda v: int(v.id) == voiceN, measure.voices))[0]
        self.id = measure.number
        self._parse_time_signature(measure, prev_ts)
        self.voices = {}
        self.bpm = prev_bpm.copy()
        self.text_marks = []

        if measure.hasVoices():
            for voice in measure.voices:
                vp = VoiceParser(voice, prev_bpm, part, measure)
                prev_bpm = vp.bpm
                self.voices[voice.id] = vp
                self.text_marks.extend(vp.text_marks)
        else:
            vp = VoiceParser(measure, prev_bpm, part, measure)
            self.bpm = vp.bpm
            self.voices["-1"] = vp
            self.text_marks.extend(vp.text_marks)
        # all voices in the measure should have the same bpm anyway

    def _parse_time_signature(self, measure, prev_ts):
        # multiple metro marks per measure are not supported for now
        if measure.timeSignature is not None:
            self.ts = TimeSignature.newFromM21TS(measure.timeSignature)
        else:
            self.ts = prev_ts

class VoiceParser:

    def __init__(self, stream, prev_bpm, part, measure):
        self.pitch = []
        self.octave = []
        self.duration = []
        self.sus = []
        self.bpm = prev_bpm.copy()
        self.part = part
        self.measure = measure
        self.text_marks = []
        self.amp = [] # TODO: implement dynamics
        for element in stream:
            self._parse_element(element)
        for el in self.pitch: self.amp.append(0.8)

    def _parse_element(self, element):

        if (not type(element) == Note
            and not type(element) == Rest
            and not type(element) == Chord
            and not type(element) == Unpitched
            and not type(element) == MetronomeMark
            and not type(element) == TextExpression):

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
        elif isinstance(element, TextExpression):
            self._parse_text(element)

    def _parse_note(self, note):
        degree = self._get_scale_degree(note.pitch)
        sus = note.quarterLength
        dur = note.quarterLength
        if degree is None:
            print("faulty element ", note)
        if note.tie is not None:
            if note.tie.type == 'start':
                sus = self._get_note_sustain(note, None)
            else:
                self.pitch.append('rest')
                self.octave.append('rest')
                self.duration.append(dur)
                self.sus.append(sus)
                return
        oct = note.octave
        self.pitch.append(degree)
        self.octave.append(oct)
        self.duration.append(dur)
        self.amp.append(note.volume.realized)
        self.sus.append(sus)


    def _parse_chord(self, chord):
        dur = chord.quarterLength
        sus = chord.quarterLength
        notes = list(chord.notes).copy()
        for note in chord.notes:
            note_sus = note.quarterLength
            if note.tie is not None:
                if note.tie.type == 'start':
                    note_sus = self._get_note_sustain(note, chord)
                else:
                    notes.remove(note)
            # foxdot can not stop one note in the chord and let the other one ring
            # i.e. it doesn't support PGroups for sustain
            # so we use the longest duration for all notes in the chord
            # (chord in music21 refers to chord, note cluster, harm. interval)
            if note_sus > sus:
                sus = note_sus
        if len(notes) > 1:
            p_map = map(lambda n: self._get_scale_degree(n.pitch), notes)
            o_map = map(lambda n: n.octave, notes)
            self.pitch.append(tuple(p_map))
            self.octave.append(tuple(o_map))
        elif len(notes) == 1:
            self.pitch.append(self._get_scale_degree(notes[0].pitch))
            self.octave.append(notes[0].octave)
        else:
            self.pitch.append('rest')
            self.octave.append('rest')

        v_map = map(lambda n: n.volume.realized, chord.notes)
        self.amp.append(tuple(v_map))
        self.duration.append(dur)
        self.sus.append(sus)


    def _parse_rest(self, rest):
        self.pitch.append('rest')
        self.octave.append('rest')
        self.duration.append(rest.quarterLength)
        self.sus.append(rest.quarterLength)
        self.amp.append(0)

    def _parse_unpitched(self, unpitched):
        self.pitch.append(self._get_scale_degree(unpitched.displayStep))
        self.octave.append(unpitched.displayOctave)
        self.duration.append(unpitched.quarterLength)
        self.sus.append(unpitched.quarterLength)

    def _parse_metro_mark(self, mm):

        self.bpm.append(self._get_bpm_from_metronome_mark(mm))

    def _parse_text(self, expression):
        text = expression.content
        m_num = expression.measureNumber
        self.text_marks.append(TextMark(text, m_num))


    # if has a tie of type 'start' we need to find the end
    # of the tie and adjust the note's duration.
    # the resulting duration may exceed the duration of the measure,
    # but that is ok in our case
    def _get_note_sustain(self, note, chord) -> float:

        cur_note = note
        cur_chord = chord
        dur = note.quarterLength
        cur_measure_index = self.part.index(self.measure)
        while cur_note is not None:
            cur_note, cur_chord, cur_measure_index = self._find_tied_note(cur_note, cur_chord, cur_measure_index)
            if cur_note == None:
                return dur
            if cur_note.tie is not None:
                if cur_note.tie.type != 'start':
                    dur += cur_note.quarterLength
                # continue looking forward until we find the tie stop
                if cur_note.tie.type == 'stop':
                    return dur
            else:
                return dur

        return dur

    # find the next note in the stream with the same pitch and duration
    # note can be part of the chord, so we need the chord object to find its position
    # in the measure
    def _find_tied_note(self, note, chord, mes_num, depth = 0):
        if mes_num == len(self.part):
            return None, None, None
        cur_measure = self.part[mes_num]
        # skip the current note

        if depth == 0:
            if note in cur_measure.elements:
                start_index = cur_measure.elements.index(note)+1
            elif (chord is not None and chord in cur_measure.elements):
                start_index = cur_measure.elements.index(chord)+1
        else:
            start_index = 0
        for next in cur_measure.elements[start_index:len(cur_measure)]:
            matching_note, matching_chord = self._find_matching_note(next, note)
            if matching_note is not None:
                return matching_note, matching_chord, mes_num
        return self._find_tied_note(note, chord, mes_num + 1, depth + 1)

    # find note with the same pitch and octave in the chord or another note
    def _find_matching_note(self, obj, note):
        if isinstance(obj, Note):
            if (obj.pitch == note.pitch and obj.octave == note.octave):
                return obj, None
        elif isinstance(obj, Chord):
            for n in obj.notes:
                if (n.pitch.name == note.pitch.name and n.octave == note.octave):
                    return n, obj
        return None, None

    def _get_scale_degree(self, pitch):
        # always use C chromatic scale for now
        scale = ChromaticScale('C')
        # scale degrees in FoxDot scales start from 0, thus -1
        return scale.getScaleDegreeFromPitch(pitch, comparisonAttribute='pitchClass') - 1

    def _get_bpm_from_metronome_mark(self, mm) -> float:
        num = float(mm.number)
        dur = float(mm.referent.quarterLength)
        return num / dur

class MidiParser:

    def __init__(self, file):
        self.score = parse_midi(file, quantizePost = False)
        self.pitch = []
        self.octave = []
        self.duration = []
        self.sus = []
        self.amp = []
        self.parse()

    # each midi file is parsed as 1 measure
    def parse(self):
        # there should always be just one part
        # the measures don't really make sense here,
        # since midi file doen't know its time signature
        # we also want to have only 1 voice, so we flatten the steam
        elements = self.score.parts[0].flatten()
        for el in elements:
            if isinstance(el, Note):
                self._parse_note(el)
            elif isinstance(el, Chord):
                self._parse_chord(el)
            elif isinstance(el, Rest):
                self._parse_rest(el)

    def _parse_note(self, note):
        next = note.next()
        self.pitch.append(self._get_scale_degree(note.pitch))
        self.octave.append(note.octave+1)
        self.sus.append(note.quarterLength)
        self.amp.append(note.volume.realized)
        if next is None:
            self.duration.append(note.quarterLength)
        else:
            self.duration.append(next.offset - note.offset)

    def _parse_chord(self, chord):
        p_map = map(lambda n: self._get_scale_degree(n.pitch), chord.notes)
        o_map = map(lambda n: n.octave+1, chord.notes)
        v_map = map(lambda n: n.volume.realized, chord.notes)
        self.pitch.append(tuple(p_map))
        self.octave.append(tuple(o_map))
        self.amp.append(tuple(v_map))
        self.duration.append(chord.quarterLength)
        self.sus.append(chord.quarterLength)

    def _parse_rest(self, rest):
        if TRIM_MIDI_CLIPS and isinstance(rest.next(), Barline):
            return
        self.pitch.append('rest')
        self.octave.append('rest')
        self.duration.append(rest.quarterLength)
        self.sus.append(rest.quarterLength)
        self.amp.append(0)

    def _get_scale_degree(self, pitch):
        # always use C chromatic scale for now
        scale = ChromaticScale('C')
        # scale degrees in FoxDot scales start from 0, thus -1
        return scale.getScaleDegreeFromPitch(pitch, comparisonAttribute='pitchClass') - 1
