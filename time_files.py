# initial setup for scoredot to run with FoxDot
sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from score import Score
from music21.stream.base import Score as M21Score
from music21 import converter
# score file path
fp = "~/Documents/time_files_full.musicxml"
# load the score into musc21
m21_score = converter.parse(fp, format = "musicxml")
instr_map = {"Sine Bass" : "midi 1", "Sine Mid" : "midi 2",
             "Sine Sub" : "midi 3", "Sine Hi" : "midi 4",
             "FB Mid" : "midi 5", "FB Hi" : "midi 6",
             "Voice Low" : "midi 7", "Voice Hi" : "midi 8",
             "E Perc" : "midi 9"}
# parse the score and assign instruments to play parts
score = Score(m21_score, instr_map)
# this gives the parts in the score
print(score.parts.keys())
Clock.now_flag = True

# Preload measures into ScoreDot
# A: measures 1 to 71. Loops until section C
sbAB = score.section(1, 4, "Sine Bass") # loop
smAB = score.section(13, 16, "Sine Mid") # loop
ssAB = score.section(19, 22, "Sine Sub") # loop
shAB = score.section(19, 22, "Sine Hi") # loop
#
ab = sbAB + smAB + ssAB + shAB
# B: 69 to 86
fbhB = score.section(69, 76, "FB Hi") # 4 times
fbmB = score.section(77, 83, "FB Mid") # once
# C: 86 to 109
vlC = score.section(90, 109, "Voice Low") # once
# D:  109 to 170
sbD1 = score.section(109, 119, "Sine Bass") # once
sbD2 = score.section(121, 124, "Sine Bass") # loop
smD1 = score.section(109, 112, "Sine Mid") # once
smD2 = score.section(114, 116, "Sine Mid") # loop
ssD = score.section(109, 116, "Sine Sub") # once
shD1 = score.section(109, 117, "Sine Hi") # play 4 times
shD2 = score.section(141, 144, "Sine Hi") # 6 times
fbhD = score.section(125, 132, "FB Hi") # 3 times
fbmD1 = score.section(109, 149, "FB Mid") # once
fbmD2 = score.section(150, 153, "FB Mid") # loop
vlD = score.section(133, 154, "Voice Low") # once
percD = score.section(109, 142, "E Perc") # once
#
d = (sbD1*1 + smD1*1 + ssD*5 + shD1*4
    + fbmD1*1 + percD*1 + ((vlD*1) % (23*4)))
sbD1 >> sbD2
smD1 >> smD2
shD1 >> shD2*6
fbmD1 >> fbmD2
dLoop = sbD2 + smD2 + fbmD2 + vlD
#
# E: measures 170 to 206
ssE = score.section(170, 181, "Sine Sub") # 5 times
shE1 = score.section(170, 173, "Sine Hi") # 4 times
shE2 = score.section(190, 193, "Sine Hi") # 4 times
smE = score.section(189, 197, "Sine Mid") # 3 times
fbhE1 = score.section(167, 173, "FB Hi") # once
fbhE2 = score.section(174, 184, "FB Hi") # 3 times
vlE1 = score.section(170, 181, "Voice Low") # once
vlE2 = score.section(182, 185, "Voice Low") # 13 times
vlE3 = score.section(186, 186, "Voice Low") # every 2 measures since 186
# F: measures 206 till the end
sh206 = score.section(206, 209, "Sine Hi") # 2 times
sh222 = score.section(222, 225, "Sine Hi") # 4 times
vl220 = score.section(220, 224, "Voice Low") # 3 times
vl228 = score.section(228, 228, "Voice Low") # overlay since 228, add octave above
vh102 = score.section(102, 102, "Voice Hi") # once or twice
vh141 = score.section(141, 145, "Voice Hi") # 2 times
