#
p1 >> MidiOut(channel = 10, oct = 3, scale = Scale.chromatic,
    degree = P[4],
    dur = P[16/4].stutter(64),
    amp = P[0.8, 1, 0.5, 0.3, 0.5, 1, 0.5, 0.8].every(2, 'shuffle'),
    bpm = linvar([2, 120], 16),
    delay = 0.5
)

p1.bpm = linvar([20, 200], 16)

p1.stop()

p2 >> MidiOut(channel = 10, oct = 3, scale = Scale.chromatic,
    degree = P[4].stutter(32),
    dur = P[1/4].stutter(32),
    amp = P[0.7, 0.4, 0.4, 0.5].everyAccompany(2, 'shuffle'),
    delay = P[0.125, 0.25, 0.5, 0.75],
    bpm = linvar([20, 300], 16),
)

p2.stop()

p3 >> MidiOut(channel = 2, oct = 3, scale = Scale.chromatic,
    degree = P[7, 6, 4,3, 0],
    dur = P[7/16, 5/16, 3/16, 4/16, 5/16, 6/16, 7/16].stutter(8),
    amp = P[0.8, 1, 0.5, 0.3, 0.8, 0.5].every(2, "shuffle"),
    bpm = linvar([100, 140], 16)
)
