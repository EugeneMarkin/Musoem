from command_map import CommandMap
from score import FileScore
from FoxDot import Pattern
from operations import Multiply

path = "/Users/eugenemarkin/Music/survival_kit"
sk = FileScore(path, None)

# saw
saw = sk["saw"]
saw.dur = 16
saw.freeze = Pattern([1.1, 1.15, 1.2, 1.05])
saw.lfohz = Pattern([0.5, 0.3, 2, 1])
saw.lfodepth = Pattern([0.2, 0.3])

# fruit
fruit = sk["fruit"]
fruit.dur = Pattern([16, 8])

# pills
pills = sk["pills"]
pills.dur = Pattern([0.5,0.333,1, 10 ,1,12, 2])
pills.freeze = 100
pills.lfohz = Pattern([0.5, 1, 5,0.2, 3])
pills.lfodepth = Pattern([0.2, 0.7, 0.5])


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

operations = {"three" : Multiply("three", 3)}

survival_kit_map = CommandMap(sk, operations)

#
