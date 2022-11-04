# An entity is anythying that can be bound to a keyword:
# Playable or Operation

class Entity(object):

    def __init__(self, keyword = "None"):
        self.keyword = keyword

    def display(self):
        return [self]

    @property
    def display_style(self):
        print("override me")
