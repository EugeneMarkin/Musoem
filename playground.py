sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from mary_lamb import mary_map
from control import MidiControl

print(mary_map.control)

from control_operations import accelerando
c = accelerando("run", 100, 200, 10)

c()


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

import numpy as np

print(np.arange(0,10)/10)

min = 5
len = 10
max = 10
l = Pattern([min + i*(max - min)/(len-1) for i in range(0, 10)])

l = (l + 5) * (5/10)

print(l)




print([i for i in range(0,10)])
