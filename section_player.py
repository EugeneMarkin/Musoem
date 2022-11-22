from FoxDot import Player


# FoxDot Player doesn't start patterns right away, instead it for several beats
# so that all patterns of the same duration will align.
# This sublass starts the pattern from the beginning, at the next beat,
# which makes sense when performing from a score

class SectionPlayer(Player):

    def count(self, time=None, event_after=False):
        return 0, self.metro.now()
