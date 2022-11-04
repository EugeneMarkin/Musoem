sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from mary_lamb import mary_map

from itertools import repeat

class MyClass:

    def __init__(self):
        self.dict = {"one" : 1, "two" : 2}

    def __getitem__(self, key):
        print("get item")
        return self.dict[key]

    def __setitem__(self, key, value):
        print("set item")
        self.dict[key] = value


my = MyClass()
my["three"] = 3
print(my["three"])



mary.player.__setattr__("degree", P[3,5,1,1])

print(mary.degree)

print(mary.player.__getattr__("degree"))

print(dict(zip([1,2,3,4,5], list(repeat("one", 5)))))
