import random

class Command:
    def __init__(self):
        self.reps = -1
        self.dynamic_changes = []
        self.actions = []

    def __str__(self):
        res = "reps: " + str(self.reps) + "\n"
        res += "dynamic_changes: " + str(self.dynamic_changes) + "\n"
        res += "actions: " + str(self.actions)
        return res

class OrList:

    def __init__(self, list):
        self.list = list

    def append(self, el):
        self.list.append(el)

    def get(self):
        return random.choice(self.list)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)