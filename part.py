# A class representing a part in the score.

# This definition of part assumes it has a single staff, e.g.
# Piano treble is one part, Piano bass is another part

# A Part contains the info of its instrument, clef, id, and metronome marks
# The actual measures containing notes belong to Voice class

# A Part either has once voice (default = -1) or can have multiple voices,
# in case of polyphonic texture for example.

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

    def _get_bpm_from_metronome_mark(self, mm) -> float:
        num = float(mm.number)
        dur = float(mm.referent.quarterLength)
        return num / dur

    @property
    def voices(self) -> [Voice]:
        return self._voices
