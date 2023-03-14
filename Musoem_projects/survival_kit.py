# Survival Kit
# parameters for the sampler instrument:
# "attack", "decay", "dur", "release", "freeze", "enhance", "teeth", "comb", "lfohz", "lfodepth", "pan", "rate", "vibRate", "vibDepth"

survival.release = 10
survival.pan = 1

backwards = ReversePitch()

elevate = Transpose(12)

saw.dur = 16
saw.freeze = P[1.1, 1.15, 1.2, 1.05]
saw.lfohz = P[0.5, 0.3, 2, 1]
saw.lfodepth = P[0.2, 0.3]

fruit.dur = P[24, 16]
fruit.freeze = P[1.11, 0.13, 0.5]
fruit.release = 4

pills.dur = P[0.5,0.333,4, 5, 6]
pills.freeze = 100
pills.lfohz = P[0.5, 1, 5,0.2, 3]
pills.lfodepth = P[0.2, 0.7, 0.5]
pi 

good.dur = P[0.5, 1, 1.5, 2]
mood.rate = P[1, -1, 0.1, -0.1, 1,1,1,-1]
shoes.freeze = 1.99
shoes.rate = P[1,-1]
cash.rate = P[1, -1]
fortune.rate = P[-0.7, 1, -1]
lord.rate = P[1, -1]

something.dur = P[4,6,8,10]
eat.freeze = 0.5
eat.vibRate = 2
eat.vibDepth = 0.8
drink.freeze = 0.6
drink.vibRate = P[0.5, 3, 1]
borrowed.vibDepth = P[0.05, 0.5, 0.03, 0.9]
worried.freeze = 0.2
old.freeze = 0.4
borrowed.vibRate = P[0.5, 3, 1]
borrowed.vibDepth = P[0.05, 0.5, 0.03, 0.9]
blue.vibRate = P[0.5, 3, 1]
blue.vibDepth = P[0.05, 0.5, 0.03, 0.9]
terrible.freeze = 0.8
worried.freeze = 0.9
mind.freeze = 1.1

best.enhance = P[8, 16, 32, 64]
best.freeze = 0.4
best.dur = 16
best.lfohz = P[0.25, 0.5, 2, 3]
best.lfodepth = 0.7

last.dur = 8
last.comb = 0.1
last.teeth = 8



your.rate = P[1, -1, 0.3, -0.3]
breath.freeze = 100
wish.freeze = 100

one.display_style = "italic"
one.freeze = 100
one.attack = 4
one.release = 6
one.dur = 2
one.lfodepth = 0
one.pan = 1
one.ordered = True

sharp.freeze = 0.5

sharp.release = 12

hundred.freeze = 0.6
hundred.release = 12

hard.freeze = 0.8
hard.release = 12

wasted.freeze = 0.4
wasted.release = 12

knife.release = 8
knife.dur = P[2, 4, 6]

bible.release = 8
bible.attack = 3
bible.dur = P[3,4,5]


dollars.dur = 3
dollars.release = 2
rubles.release = 4
stone.release = 4
truth.release = 4
youth.release = 4
bright.release = 4
flash.release = 4
blast.release = 4
wave.release = 4
father.release = 4
son.release = 4
holy.release = 4
ghost.release = 4
