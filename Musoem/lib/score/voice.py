# A class representing a single voice of a single part

# A Voice does not need to be monophonic, i.e. it can contain chords,
# note clusters, etc.

# Unless the piece is polyphonic and 'voices' feature of music engraving software
# is used, a voice will normally correspond to a separate staff of an instrument part,
# e.g. piano treble or piano bass or violin
from .measure import Measure
from ..playables.section import Section

class Voice:

    # Initializer takes a list of Measure objects, which are created during parsing in
    # Part class initialization
    # TODO: should the parsing be happening elsewhere?
    def __init__(self, id, measures_list: [Measure], instrument):
        self.id = id
        self._measures = measures_list
        self.instrument = instrument

    # Append a measure to the voice
    def append(self, mes: Measure):
        self._measures.append(mes)
    # Get a Section object from this voice, containing a range of measures
    def section(self, from_measure: int, to_measure: int) -> Section:
        return Section(self._measures[from_measure-1:to_measure], self.instrument)
    # Get a Section object containing ALL the measures in this voice
    @property
    def all(self) -> Section:
        return Section(self._measures, self.instrument)

    # Get the measures list of this voice
    @property
    def measures(self):
        return self._measures
