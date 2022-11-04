# initial setup for scoredot to run with FoxDot
sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from score import Score
from music21.stream.base import Score as M21Score
from music21 import converter

from myclick import Click

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
# A: "Time flies" measures 1 to 71. Loops until section C
sbAB = score.section(1, 4, "Sine Bass") # loop
smAB = score.section(13, 16, "Sine Mid") # loop
ssAB = score.section(19, 22, "Sine Sub") # loop
shAB = score.section(19, 22, "Sine Hi") # loop
percA = score.section(13, 13 , "E Perc") # loop
percA.bpm = 180
percB = score.section(42, 44, "E Perc") # loop
#
ab = sbAB + smAB + ssAB + shAB
#
clickA = Click(120)
#
time_flies = (sbAB * -1) + ((smAB % (12*4))*-1) + ((ssAB % (18*4))*-1) + ((shAB % (12*4))*-1) + clickA
# B "Time waits": 69 to 86
fbhB = score.section(69, 76, "FB Hi") # 4 times
fbmB = score.section(77, 83, "FB Mid") # once
clickB = Click(80)
#
time_waits = (fbhB*4) + (fbmB % 32)*1 + clickB
# C: "Time lies": 86 to 109
vlC = score.section(90, 109, "Voice Low") # once
#
time_lies = vlC*1
# D: "Time fails"  109 to 170
sbD1 = score.section(108, 119, "Sine Bass") # once
sbD2 = score.section(121, 124, "Sine Bass") # loop
smD1 = score.section(108, 112, "Sine Mid") # once
smD2 = score.section(114, 116, "Sine Mid") # loop
ssD = score.section(108, 116, "Sine Sub") # 5 times
shD1 = score.section(108, 117, "Sine Hi") # play 4 times
shD2 = score.section(141, 144, "Sine Hi") # 6 times
fbhD = score.section(125, 132, "FB Hi") # 3 times
fbmD1 = score.section(108, 149, "FB Mid") # once
fbmD2 = score.section(150, 153, "FB Mid") # loop
vlD = score.section(133, 154, "Voice Low") # once
percD = score.section(108, 142, "E Perc") # once
clickD = Click(94)
#
d = (sbD1*1) + (smD1*1) + (ssD*5) + (shD1*4) + (fbhD % (16 * 4)) * 3 + (fbmD1*1) + (percD*1) + ((vlD % (23*4))*1) + clickD + (percD % (13*4))
sbD1 >> sbD2
smD1 >> smD2
shD1 >> (shD2*6)
fbmD1 >> fbmD2*2
dLoop = sbD2 + smD2 + fbmD2 + vlD
time_fails = d
time_trembles = sbD2 + smD2 + fbmD2 + vlD + clickD
#
# E: "Time dies" measures 170 to 206
ssE = score.section(170, 181, "Sine Sub") # 5 times
shE1 = score.section(170, 173, "Sine Hi") # 4 times
shE2 = score.section(190, 193, "Sine Hi") # 4 times
smE = score.section(189, 197, "Sine Mid") # 3 times
fbhE1 = score.section(167, 173, "FB Hi") # once
fbhE2 = score.section(174, 184, "FB Hi") # 3 times
vlE1 = score.section(170, 181, "Voice Low") # once
vlE2 = score.section(182, 185, "Voice Low") # 13 times
vlE3 = score.section(186, 186, "Voice Low") # every 2 measures since 186
percE = score.section(169, 227, "E Perc") # once
clickE = Click(94)
time_dies = sbD2 + (ssE*5) + (shE1*4) + (shE2*4) + ((smE % (18*4))*3) + (fbhE1*1) + ((fbhE2 % 16)*3) + (vlE1*1) + (vlE2*13) + (percE*1) + clickE
voice = vlE3
# F: "Time lives" measures 206 till the end
sh206 = score.section(206, 209, "Sine Hi") # 2 times
sh222 = score.section(222, 225, "Sine Hi") # 4 times
vl220 = score.section(220, 224, "Voice Low") # 3 times
vl228 = score.section(228, 228, "Voice Low") # overlay since 228, add octave above
#
time_lives = (sh206*2) + ((vl220 % (14 * 4))*4)
sh206 >> (sh222*4)
other_voice = vl228
