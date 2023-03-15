all_sounds.slide = 1
all_sections.fmod = 2
all_samples.freeze = 1.5

all_with_instrument("sampler").comb = 0.7
all_with_instrument("midi 1").sus = 2

reverse = ReversePitch()
backwards = Retrograde()
elevate = Transpose(12)
down = Transpose(-12)
