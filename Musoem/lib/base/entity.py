# An entity is anythying that can be bound to a keyword:
# Playable or Operation

class Entity(object):

    def __init__(self, keyword = "None"):
        self.__dict__["keyword"] = keyword
        self.__dict__["display_style"] = "normal"

    def display(self):
        return [self]
