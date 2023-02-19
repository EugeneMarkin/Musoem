from section_player import SectionPlayer
from FoxDot import MidiOut
from section import Section
from FoxDot import Pattern

class Click(Section):

    def __init__(self, bpm):
        super().__init__([], "midi 10")
        self.degree = Pattern([0,1,1,1])
        self.oct = Pattern([3])
        self.dur = Pattern([1])
        self.bpm = Pattern([bpm])
