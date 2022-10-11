"""
section(N): play section N times, loop if N is None
 >> : play next section after this one stops playing
 * : play section N times
 + : start the right section when the left section starts
 ~ : stop playing section
 % : delay the start of the section by N beats
 """
sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from control import Control
from control import Tremolo
from control import Wave
from control import Mic
from myclick import Click

tempo = Control(0, 80, 120, 120)
pulse = Tremolo(1, 0, 1, 3/4)
wave = Wave(2, 0, 1, "sine")
depth = Control(3, 0, 1, 0.5)
jitter = Control(4, 0, 1, 0.5)
comb = Control(5, 0, 1, 0.8)
overdrive = Control(6, 0, 1, 0.4)
delay = Control(7, 0, 5, 0)
feedback = Control(8, 0, 1, 0.5)
ring = Control(9, 0, 1, 0)
redux = Control(10, 0, 1, 0)
low_pulse = Tremolo(11, 0, 1, 1/2)
wave2 = Wave(12, 0, 1, "triangle")
jitter2 = Control(13, 0, 1, 0)
mid_pulse = Tremolo(14, 0, 1, 1)
hi_pulse = Tremolo(15, 0, 1, 1/3)
mic = Mic(16, 0, 1, 0)
def reset():
    pulse(3/4)
    wave("sine")
    depth(0.5)
    jitter(0.02)
    comb(0.8)
    overdrive(0.4)
    delay(0.1)
    feedback(0.5)
    ring(0.02)
    redux(0.02)
    low_pulse(1/2)
    wave2("triangle")
    jitter2(0.02)
    mid_pulse(1)
    hi_pulse(1/3)
