from FoxDot import Pattern
from lib.command.command_map import CommandMap
from lib.score.score import FileScore

from lib.operations.operations import Multiply

path = "/Users/eugenemarkin/Music/survival_kit"
sk = FileScore(path, None)

sk["survival"].release = 10
sk["survival"].pan = 1
# saw
saw = sk["saw"]
saw.dur = 16
saw.freeze = Pattern([1.1, 1.15, 1.2, 1.05])
saw.lfohz = Pattern([0.5, 0.3, 2, 1])
saw.lfodepth = Pattern([0.2, 0.3])

# fruit
fruit = sk["fruit"]
fruit.dur = Pattern([24, 16])
fruit.freeze = Pattern([1.11, 0.13, 0.5])
fruit.release = 4

# pills
pills = sk["pills"]
pills.dur = Pattern([0.5,0.333,4 ,5, 6])
pills.freeze = 100
pills.lfohz = Pattern([0.5, 1, 5,0.2, 3])
pills.lfodepth = Pattern([0.2, 0.7, 0.5])
pills.release = 5

sk["anything"].dur = 8


# good
good = sk["good"]
good.dur = Pattern([0.5, 1, 1.5, 2])
sk["mood"].rate = Pattern([1, -1, 0.1, -0.1, 1,1,1,-1])
sk["shoes"].freeze = 1.99
sk["shoes"].rate = Pattern([1,-1])
sk["cash"].rate = Pattern([1, -1])
sk["fortune"].rate = Pattern([-0.7, 1, -1])
sk["lord"].rate = Pattern([1, -1])

#something
something = sk["something"]
something.dur = Pattern([4,6,8,10])
eat = sk["eat"]
eat.freeze = 0.5
eat.vibRate = 2
eat.vibDepth = 0.8
sk["drink"].freeze = 0.6
sk["borrowed"].vibRate = Pattern([0.5, 3, 1])
sk["borrowed"].vibDepth = Pattern([0.05, 0.5, 0.03, 0.9])
sk["worried"].freeze = 0.2
sk["old"].freeze = 0.4
sk["borrowed"].vibRate = Pattern([0.5, 3, 1])
sk["borrowed"].vibDepth = Pattern([0.05, 0.5, 0.03, 0.9])
sk["blue"].vibRate = Pattern([0.5, 3, 1])
sk["blue"].vibDepth = Pattern([0.05, 0.5, 0.03, 0.9])
sk["terrible"].freeze = 0.8
sk["worried"].freeze = 0.9
sk["mind"].freeze = 1.1


best = sk["best"]
best.enhance = Pattern([8, 16, 32, 64])
best.freeze = 0.4
best.dur = 16
best.lfohz = Pattern([0.25, 0.5, 2, 3])
best.lfodepth = 0.7

last = sk["last"]
last.dur = 8
last.comb = 0.1
last.teeth = 8



sk["your"].rate = Pattern([1, -1, 0.3, -0.3])
sk["breath"].freeze = 100
sk["wish"].freeze = 100

one = sk["one"]
one.display_style = "italic"
one.freeze = 100
one.attack = 4
one.release = 6
one.dur = 2
one.lfodepth = 0
one.pan = 1
one.ordered = True

sk["sharp"].freeze = 0.5

sk["sharp"].release = 12

sk["hundred"].freeze = 0.6
sk["hundred"].release = 12

sk["hard"].freeze = 0.8
sk["hard"].release = 12

sk["wasted"].freeze = 0.4
sk["wasted"].release = 12

sk["knife"].release = 8
sk["knife"].dur = Pattern([2, 4, 6])

sk["bible"].release = 8
sk["bible"].attack = 3
sk["bible"].dur = Pattern([3,4,5])


sk["dollars"].dur = 3
sk["dollars"].release = 2
sk["rubles"].release = 4
sk["stone"].release = 4
sk["truth"].release = 4
sk["youth"].release = 4
sk["bright"].release = 4
sk["flash"].release = 4
sk["blast"].release = 4
sk["wave"].release = 4
sk["father"].release = 4
sk["son"].release = 4
sk["holy"].release = 4
sk["ghost"].release = 4

operations = {"three" : Multiply("three", 3)}

survival_kit_map = CommandMap(sk, operations)

#
